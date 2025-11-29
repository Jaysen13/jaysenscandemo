package com.springboot.springbootdemo.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;

@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("项目API文档")  // 文档标题
                        .version("1.0.0")     // 版本
                        .description("API接口说明文档")  // 描述
                );
    }
    // 2. 配置全局路径匹配（核心）
    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.OAS_30) // 指定 Swagger3 版本
                .select()
                // 扫描指定包下的接口（基础过滤）
                .apis(RequestHandlerSelectors.basePackage("com.springboot.springbootdemo.controller"))
                // 只匹配路径以 /api/ 开头的接口（关键：定义Swagger要展示的路径前缀）
                .paths(PathSelectors.ant("/vuln/api/**"))
                // 可选：排除某些路径（如内部接口）
                // .paths(PathSelectors.not(PathSelectors.ant("/api/internal/**")))
                .build();
    }
}