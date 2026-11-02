# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI08-001 | PyTorch MLP 매출 예측 | 전처리기 로드 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-002 | PyTorch MLP 매출 예측 | 가중치 로드 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-003 | PyTorch MLP 매출 예측 | model.eval | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-004 | PyTorch MLP 매출 예측 | 모델 캐시 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-005 | PyTorch MLP 매출 예측 | 1행 매출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-006 | PyTorch MLP 매출 예측 | 5행 매출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-007 | PyTorch MLP 매출 예측 | 로그 역변환 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-008 | PyTorch MLP 매출 예측 | 음수 예측 방어 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-009 | PyTorch MLP 매출 예측 | 0 예측 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-010 | PyTorch MLP 매출 예측 | 소수 한 자리 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-011 | PyTorch MLP 매출 예측 | 입력 dtype | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-012 | PyTorch MLP 매출 예측 | 배치 100행 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-013 | PyTorch MLP 매출 예측 | 모델 파일 누락 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-014 | PyTorch MLP 매출 예측 | 전처리기 누락 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-015 | PyTorch MLP 매출 예측 | state dict 불일치 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-018 | PyTorch MLP 매출 예측 | 예측 재현성 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-019 | PyTorch MLP 매출 예측 | 메모리 누수 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI08-020 | PyTorch MLP 매출 예측 | 컨테이너 CPU 환경 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## AI08-001 전처리기 로드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 전처리기 로드 joblib preprocessor type=ColumnTransformer cached=ColumnTransformer transform=True

## AI08-002 가중치 로드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 가중치 로드 torch.load kwargs={'map_location': 'cpu', 'weights_only': True} path=/Users/jeong-yelim/orca/dasigolmok_v2/ai/models/sales_mlp.pt training=False

## AI08-003 model.eval
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 평가 모드 model.training=False dropout_count=1 dropout_training=[False]

## AI08-004 모델 캐시
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 두 번 추론 torch.load=1 joblib.load=1

## AI08-005 1행 매출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 1행 매출=[5584.7]

## AI08-006 5행 매출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 5행 batch=[5584.6, 5530.5, 5476.8, 5423.7, 5371.1] singles=[5584.7, 5530.5, 5476.8, 5423.7, 5371.1] 최근접위치=[0, 1, 2, 3, 4]

## AI08-007 로그 역변환
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: log1p(100)=4.615121 expm1 후 예측=[100.0]

## AI08-008 음수 예측 방어
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 음수 복원 inverse=-10 → [0.0]

## AI08-009 0 예측
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 영 로그 복원 output log=0 → [0.0]

## AI08-010 소수 한 자리
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 예측 333.33 → [333.3]

## AI08-011 입력 dtype
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 모델 입력 dtype=torch.float32 shape=(1, 134)

## AI08-012 배치 100행
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 100행 결과=100 min=4796.1 max=5584.6 latency=0.006s peak=0.2MB

## AI08-013 모델 파일 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: sales_mlp.pt 없음 → FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/qp/wtpnyvgn0kx_759hkfcdztw80000gn/T/pytest-of-jeong-yelim/pytest-3/test_AI08_0130/sales_mlp.pt'

## AI08-014 전처리기 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: preprocessor 없음 → FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/qp/wtpnyvgn0kx_759hkfcdztw80000gn/T/pytest-of-jeong-yelim/pytest-3/test_AI08_0140/sales_mlp_preprocessor.joblib'

## AI08-015 state dict 불일치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: input_size 불일치 → RuntimeError: Error(s) in loading state_dict for SalesMLP: size mismatch for layers.0.weight: copying a param with shape torch.Size([64, 64]) from checkpoint, the shape in current model is torc

## AI08-018 예측 재현성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 1회=[5130.4] 2회=[5130.4] eval=True

## AI08-019 메모리 누수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 1000회 grad_enabled=False requires_grad=False param_grad_any=False peak=0.4MB

## AI08-020 컨테이너 CPU 환경
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: parameter.device=cpu cuda_available=False map_location 코드경로=cpu
