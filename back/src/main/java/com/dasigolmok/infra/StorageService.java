package com.dasigolmok.infra;

import com.dasigolmok.global.exception.BusinessException;
import com.dasigolmok.global.response.ErrorCode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Locale;
import java.util.Set;
import java.util.UUID;

@Service
public class StorageService {

    private static final Set<String> ALLOWED_TYPES = Set.of("image/jpeg", "image/png", "image/webp", "image/gif");
    private static final long MAX_SIZE = 5 * 1024 * 1024;

    private final Path uploadPath;

    public StorageService(@Value("${app.upload.dir}") String uploadDir) throws IOException {
        this.uploadPath = Paths.get(uploadDir).toAbsolutePath().normalize();
        Files.createDirectories(this.uploadPath);
    }

    public String saveImage(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new BusinessException(ErrorCode.VALIDATION_ERROR, "이미지 파일이 필요합니다.");
        }
        if (!ALLOWED_TYPES.contains(file.getContentType())) {
            throw new BusinessException(ErrorCode.VALIDATION_ERROR, "지원하지 않는 이미지 형식입니다.");
        }
        if (file.getSize() > MAX_SIZE) {
            throw new BusinessException(ErrorCode.VALIDATION_ERROR, "이미지 크기는 5MB 이하여야 합니다.");
        }

        byte[] header = readHeader(file, 16);
        String detected = detectImageType(header);
        if (detected == null) {
            throw new BusinessException(ErrorCode.VALIDATION_ERROR, "이미지 magic byte 검증에 실패했습니다. 실행파일·위장 업로드는 거부됩니다.");
        }
        if (!contentTypeMatches(file.getContentType(), detected)) {
            throw new BusinessException(ErrorCode.VALIDATION_ERROR, "Content-Type과 파일 시그니처가 일치하지 않습니다.");
        }

        String ext = extensionFor(detected, file.getOriginalFilename());
        String filename = UUID.randomUUID() + ext;
        Path target = uploadPath.resolve(filename);
        try {
            file.transferTo(target);
        } catch (IOException e) {
            throw new BusinessException(ErrorCode.INTERNAL_ERROR, "이미지 저장에 실패했습니다.");
        }
        return "/uploads/" + filename;
    }

    private byte[] readHeader(MultipartFile file, int size) {
        try (InputStream in = file.getInputStream()) {
            return in.readNBytes(size);
        } catch (IOException e) {
            throw new BusinessException(ErrorCode.VALIDATION_ERROR, "파일을 읽을 수 없습니다.");
        }
    }

    private String detectImageType(byte[] b) {
        if (b.length >= 3 && (b[0] & 0xFF) == 0xFF && (b[1] & 0xFF) == 0xD8 && (b[2] & 0xFF) == 0xFF) {
            return "jpeg";
        }
        if (b.length >= 8
                && b[0] == (byte) 0x89 && b[1] == 0x50 && b[2] == 0x4E && b[3] == 0x47
                && b[4] == 0x0D && b[5] == 0x0A && b[6] == 0x1A && b[7] == 0x0A) {
            return "png";
        }
        if (b.length >= 6
                && b[0] == 'G' && b[1] == 'I' && b[2] == 'F'
                && b[3] == '8' && (b[4] == '7' || b[4] == '9') && b[5] == 'a') {
            return "gif";
        }
        if (b.length >= 12
                && b[0] == 'R' && b[1] == 'I' && b[2] == 'F' && b[3] == 'F'
                && b[8] == 'W' && b[9] == 'E' && b[10] == 'B' && b[11] == 'P') {
            return "webp";
        }
        return null;
    }

    private boolean contentTypeMatches(String contentType, String detected) {
        if (contentType == null) {
            return false;
        }
        String ct = contentType.toLowerCase(Locale.ROOT);
        return switch (detected) {
            case "jpeg" -> ct.contains("jpeg") || ct.contains("jpg");
            case "png" -> ct.contains("png");
            case "gif" -> ct.contains("gif");
            case "webp" -> ct.contains("webp");
            default -> false;
        };
    }

    private String extensionFor(String detected, String originalFilename) {
        return switch (detected) {
            case "png" -> ".png";
            case "gif" -> ".gif";
            case "webp" -> ".webp";
            default -> {
                if (originalFilename != null && originalFilename.toLowerCase(Locale.ROOT).endsWith(".jpeg")) {
                    yield ".jpeg";
                }
                yield ".jpg";
            }
        };
    }
}
