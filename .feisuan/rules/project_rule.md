
# 开发规范指南
为保证代码质量、可维护性、安全性与可扩展性，请在开发过程中严格遵循以下规范。

## 一、项目环境

- **操作系统版本**：Windows 11
- **工作区路径**：E:\java_project\springbootdemo
- **语言版本**：Java 17.0.15
- **构造工具**：Maven
- **代码作者**：lsj31

## 二、技术栈要求

- **主框架**：Spring Boot 2.7.0 (基于项目配置文件)
- **核心依赖**：
  - `spring-boot-starter-web`
  - `spring-boot-starter-jdbc`
  - `spring-boot-starter-log4j2`
  - `druid-spring-boot-starter`
  - `springfox-boot-starter`
  - `spring-boot-starter-thymeleaf`
  - `lombok`

## 三、目录结构

```
springbootdemo
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com
│   │   │       └── springboot
│   │   │           └── springbootdemo
│   │   │               ├── config
│   │   │               ├── controller
│   │   │               └── util
│   │   └── resources
│   │       ├── static
│   │       └── templates
│   └── test
```

## 四、分层架构规范

| 层级        | 职责说明                         | 开发约束与注意事项                                               |
|-------------|----------------------------------|----------------------------------------------------------------|
| **Controller** | 处理 HTTP 请求与响应，定义 API 接口 | 不得直接访问数据库，必须通过 Service 层调用                  |
| **Service**    | 实现业务逻辑、事务管理与数据校验   | 必须通过 Repository 层访问数据库；返回 DTO 而非 Entity（除非必要） |
| **Repository** | 数据库访问与持久化操作             | 使用 `JdbcTemplate` 或自定义 Repository；使用 `@EntityGraph` 避免 N+1 查询问题     |
| **Entity**     | 映射数据库表结构                   | 不得直接返回给前端（需转换为 DTO）；包名统一为 `entity`         |

### 接口与实现分离

- 所有接口实现类需放在接口所在包下的 `impl` 子包中。

## 五、安全与性能规范

### 输入校验

- 使用 `@Valid` 与 JSR-303 校验注解（如 `@NotBlank`, `@Size` 等）
  - 注意：Spring Boot 2.7.0 中校验注解位于 `javax.validation.constraints.*`

- 禁止手动拼接 SQL 字符串，防止 SQL 注入攻击。

### 事务管理

- `@Transactional` 注解仅用于 **Service 层**方法。
- 避免在循环中频繁提交事务，影响性能。

### 性能优化

- 使用 Druid 连接池进行数据库连接管理，配置合理的初始连接数、最大连接数、最小空闲连接数等。
- 使用 `@EntityGraph` 或 `JdbcTemplate` 来避免 N+1 查询问题。

## 六、代码风格规范

### 命名规范

| 类型       | 命名方式             | 示例                  |
|------------|----------------------|-----------------------|
| 类名       | UpperCamelCase       | `UserServiceImpl`     |
| 方法/变量  | lowerCamelCase       | `saveUser()`          |
| 常量       | UPPER_SNAKE_CASE     | `MAX_LOGIN_ATTEMPTS`  |

### 注释规范

- 所有类、方法、字段需添加 **Javadoc** 注释。
- 注释使用中文进行描述。

### 类型命名规范（阿里巴巴风格）

| 后缀 | 用途说明                     | 示例         |
|------|------------------------------|--------------|
| DTO  | 数据传输对象                 | `UserDTO`    |
| DO   | 数据库实体对象               | `UserDO`     |
| BO   | 业务逻辑封装对象             | `UserBO`     |
| VO   | 视图展示对象                 | `UserVO`     |
| Query| 查询参数封装对象             | `UserQuery`  |

### 实体类简化工具

- 使用 Lombok 注解替代手动编写 getter/setter/构造方法：
  - `@Data`
  - `@NoArgsConstructor`
  - `@AllArgsConstructor`

## 七、扩展性与日志规范

### 接口优先原则

- 所有业务逻辑通过接口定义（如 `UserService`），具体实现放在 `impl` 包中（如 `UserServiceImpl`）。

### 日志记录

- 使用 `@Slf4j` 注解代替 `System.out.println`

## 八、编码原则总结

| 原则       | 说明                                       |
|------------|--------------------------------------------|
| **SOLID**  | 高内聚、低耦合，增强可维护性与可扩展性     |
| **DRY**    | 避免重复代码，提高复用性                   |
| **KISS**   | 保持代码简洁易懂                           |
| **YAGNI**  | 不实现当前不需要的功能                     |
| **OWASP**  | 防范常见安全漏洞，如 SQL 注入、XSS 等      |

## 九、其他注意事项

- 项目中使用了可能存在安全漏洞的 Log4j2 版本（2.14.1），建议升级到最新稳定版本以避免潜在的安全风险。
- MySQL 驱动版本为 8.0.33，请确保数据库兼容性。
- 请定期检查和更新项目的依赖版本，以获得最新的安全补丁和功能改进。
