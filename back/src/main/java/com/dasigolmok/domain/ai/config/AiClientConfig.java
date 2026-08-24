package com.dasigolmok.domain.ai.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.web.client.ClientHttpRequestFactories;
import org.springframework.boot.web.client.ClientHttpRequestFactorySettings;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.ClientHttpRequestFactory;
import org.springframework.web.client.RestClient;

import java.time.Duration;

@Configuration
public class AiClientConfig {

    @Bean
    @ConditionalOnProperty(name = "app.ai.adapter", havingValue = "fastapi")
    public RestClient aiRestClient(AiProperties aiProperties) {
        ClientHttpRequestFactory factory = ClientHttpRequestFactories.get(
                ClientHttpRequestFactorySettings.DEFAULTS
                        .withConnectTimeout(Duration.ofMillis(aiProperties.getConnectTimeoutMs()))
                        .withReadTimeout(Duration.ofMillis(aiProperties.getReadTimeoutMs())));
        return RestClient.builder()
                .baseUrl(aiProperties.getBaseUrl())
                .requestFactory(factory)
                .build();
    }
}
