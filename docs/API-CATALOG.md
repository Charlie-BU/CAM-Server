# Service SubRouter API

## GetServiceById

- API 名称：GetServiceById
- 请求方法与路径：GET /v1/service/getServiceById
- 接口等级：P2
- 接口描述：根据服务 ID 查询服务完整详情。
- 请求参数：
  - Query 参数：
    - id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get service success。
    - service：object 类型，必填、不可为 null、描述：服务详情、示例值：见响应示例。
- service 类型：
  - id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - owner_id：int 类型，必填、不可为 null、描述：服务所有者 ID、示例值：1。
  - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
  - version：string 类型，必填、不可为 null、描述：当前版本、示例值：1.0.0。
  - description：string 类型，可为 null、描述：服务说明、示例值：订单服务。
  - created_at：string 类型，必填、不可为 null、描述：创建时间（ISO 8601）、示例值：2026-09-02T10:00:00。
  - updated_at：string 类型，必填、不可为 null、描述：更新时间（ISO 8601）、示例值：2026-09-02T10:00:00。
  - is_deleted：boolean 类型，必填、不可为 null、描述：是否软删除、示例值：false。
  - deleted_at：string 类型，可为 null、描述：软删除时间、示例值：null。
  - owner：object 类型，必填、不可为 null、描述：所有者信息、示例值：{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"}。
  - maintainers：array 类型，必填、不可为 null、描述：维护者列表、示例值：[]。
  - api_categories：array 类型，必填、不可为 null、描述：API 分类列表、示例值：[]。
  - apis：array 类型，必填、不可为 null、描述：正式 API 简表、示例值：[]。
  - iterations：array 类型，必填、不可为 null、描述：服务迭代列表、示例值：[]。
- owner 类型：
  - id：int 类型，必填、不可为 null、描述：用户 ID、示例值：1。
  - username：string 类型，必填、不可为 null、描述：用户名、示例值：alice。
  - nickname：string 类型，可为 null、描述：昵称、示例值：Alice。
  - email：string 类型，可为 null、描述：邮箱、示例值：alice@example.com。
  - role：string 类型，必填、不可为 null、描述：角色、示例值：backend。
  - level：int 类型，必填、不可为 null、描述：用户等级、示例值：4。
  - created_at：string 类型，必填、不可为 null、描述：用户创建时间、示例值：2026-09-02T10:00:00。
- maintainers 元素类型：
  - id：int 类型，必填、不可为 null、描述：用户 ID、示例值：2。
  - username：string 类型，必填、不可为 null、描述：用户名、示例值：bob。
  - nickname：string 类型，可为 null、描述：昵称、示例值：Bob。
  - email：string 类型，可为 null、描述：邮箱、示例值：bob@example.com。
  - role：string 类型，必填、不可为 null、描述：角色、示例值：frontend。
  - level：int 类型，必填、不可为 null、描述：用户等级、示例值：4。
  - created_at：string 类型，必填、不可为 null、描述：用户创建时间、示例值：2026-09-02T10:00:00。

请求示例：

GET /v1/service/getServiceById?id=101

响应值示例：

{"status":200,"message":"Get service success","service":{"id":101,"owner_id":1,"service_uuid":"order-service","version":"1.0.0","description":"订单服务","created_at":"2026-09-02T10:00:00","updated_at":"2026-09-02T10:00:00","is_deleted":false,"deleted_at":null,"owner":{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"},"maintainers":[],"api_categories":[],"apis":[],"iterations":[]}}

## GetAllServices

- API 名称：GetAllServices
- 请求方法与路径：GET /v1/service/getAllServices
- 接口等级：P1
- 接口描述：分页查询所有服务，只有 L0 用户可调用，结果包含已软删除服务。
- 请求参数：
  - Query 参数：
    - page_size：int 类型，可选、不可为 null、描述：每页数量，默认值：10、示例值：20。
    - current_page：int 类型，可选、不可为 null、描述：页码，默认值：1、示例值：1。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get services success。
    - services：array 类型，必填、不可为 null、描述：服务列表、示例值：见响应示例。
    - total：int 类型，必填、不可为 null、描述：全部服务总数、示例值：1。
- services 元素类型：
  - id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
  - version：string 类型，必填、不可为 null、描述：版本、示例值：1.0.0。
  - description：string 类型，可为 null、描述：服务说明、示例值：订单服务。
  - owner_id：int 类型，必填、不可为 null、描述：所有者 ID、示例值：1。
  - owner：object 类型，必填、不可为 null、描述：所有者信息，含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":0,"created_at":"2026-09-02T10:00:00"}。
  - created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - is_deleted：boolean 类型，必填、不可为 null、描述：是否软删除、示例值：false。
  - deleted_at：string 类型，可为 null、描述：删除时间、示例值：null。

请求示例：

GET /v1/service/getAllServices?page_size=20&current_page=1

响应值示例：

{"status":200,"message":"Get services success","services":[{"id":101,"service_uuid":"order-service","version":"1.0.0","description":"订单服务","owner_id":1,"owner":{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":0,"created_at":"2026-09-02T10:00:00"},"created_at":"2026-09-02T10:00:00","is_deleted":false,"deleted_at":null}],"total":1}

## GetHisNewestServicesByOwnerId

- API 名称：GetHisNewestServicesByOwnerId
- 请求方法与路径：GET /v1/service/getHisNewestServicesByOwnerId
- 接口等级：P2
- 接口描述：分页查询指定所有者的未删除最新服务；查询自身时由令牌确定所有者。
- 请求参数：
  - Query 参数：
    - is_my_services：boolean 类型，可选、不可为 null、描述：是否查询当前用户服务，默认值：true、示例值：false。
    - owner_id：int 类型，当 is_my_services 为 false 时必填、不可为 null、描述：目标所有者 ID、示例值：1。
    - page_size：int 类型，可选、不可为 null、描述：每页数量，默认值：10、示例值：10。
    - current_page：int 类型，可选、不可为 null、描述：页码，默认值：1、示例值：1。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get services success。
    - services：array 类型，必填、不可为 null、描述：最新服务列表、示例值：见响应示例。
    - total：int 类型，必填、不可为 null、描述：服务总数、示例值：1。
- services 元素类型：
  - id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
  - version：string 类型，必填、不可为 null、描述：当前版本、示例值：1.0.0。
  - description：string 类型，可为 null、描述：服务说明、示例值：订单服务。
  - owner_id：int 类型，必填、不可为 null、描述：所有者 ID、示例值：1。
  - owner：object 类型，查询他人时返回、可为 null、描述：所有者信息，含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"}。
  - created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - is_deleted：boolean 类型，必填、不可为 null、描述：是否软删除、示例值：false。

请求示例：

GET /v1/service/getHisNewestServicesByOwnerId?is_my_services=false&owner_id=1&page_size=10&current_page=1

响应值示例：

{"status":200,"message":"Get services success","services":[{"id":101,"service_uuid":"order-service","version":"1.0.0","description":"订单服务","owner_id":1,"owner":{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"},"created_at":"2026-09-02T10:00:00","is_deleted":false}],"total":1}

## GetHisMaintainedServicesByUserId

- API 名称：GetHisMaintainedServicesByUserId
- 请求方法与路径：GET /v1/service/getHisMaintainedServicesByUserId
- 接口等级：P2
- 接口描述：分页查询用户作为维护者的未删除服务。
- 请求参数：
  - Query 参数：
    - user_id：int 类型，可选、不可为 null、描述：维护者用户 ID，默认值：当前用户 ID、示例值：2。
    - page_size：int 类型，可选、不可为 null、描述：每页数量，默认值：10、示例值：10。
    - current_page：int 类型，可选、不可为 null、描述：页码，默认值：1、示例值：1。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get services success。
    - services：array 类型，必填、不可为 null、描述：维护的服务列表、示例值：见响应示例。
    - total：int 类型，必填、不可为 null、描述：服务总数、示例值：1。
- services 元素类型：
  - id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
  - version：string 类型，必填、不可为 null、描述：版本、示例值：1.0.0。
  - description：string 类型，可为 null、描述：服务说明、示例值：订单服务。
  - owner_id：int 类型，必填、不可为 null、描述：所有者 ID、示例值：1。
  - owner：object 类型，必填、不可为 null、描述：所有者信息，含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"}。
  - created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - is_deleted：boolean 类型，必填、不可为 null、描述：是否软删除、示例值：false。

请求示例：

GET /v1/service/getHisMaintainedServicesByUserId?user_id=2&page_size=10&current_page=1

响应值示例：

{"status":200,"message":"Get services success","services":[{"id":101,"service_uuid":"order-service","version":"1.0.0","description":"订单服务","owner_id":1,"owner":{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"},"created_at":"2026-09-02T10:00:00","is_deleted":false}],"total":1}

## GetServiceByUuidAndVersion

- API 名称：GetServiceByUuidAndVersion
- 请求方法与路径：GET /v1/service/getServiceByUuidAndVersion
- 接口等级：P2
- 接口描述：按服务 UUID 和版本查询服务快照；version 为 latest 时查询当前版本。
- 请求参数：
  - Query 参数：
    - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
    - version：string 类型，必填、不可为 null、描述：服务版本或 latest、示例值：1.0.0。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get service success。
    - service：object 类型，必填、不可为 null、描述：当前 Service 或历史 ServiceIteration 快照、示例值：见响应示例。
    - is_latest：boolean 类型，必填、不可为 null、描述：是否当前版本、示例值：true。
- service 类型：
  - 当前版本 id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - 当前版本 owner_id：int 类型，必填、不可为 null、描述：所有者 ID、示例值：1。
  - 当前版本 service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
  - 当前版本 version：string 类型，必填、不可为 null、描述：服务版本、示例值：1.0.0。
  - 当前版本 description：string 类型，可为 null、描述：服务说明、示例值：订单服务。
  - 当前版本 created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - 当前版本 updated_at：string 类型，必填、不可为 null、描述：更新时间、示例值：2026-09-02T10:00:00。
  - 当前版本 is_deleted：boolean 类型，必填、不可为 null、描述：是否软删除、示例值：false。
  - 当前版本 deleted_at：string 类型，可为 null、描述：软删除时间、示例值：null。
  - 当前版本 owner：object 类型，必填、不可为 null、描述：所有者，含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"}。
  - 当前版本 maintainers：array 类型，必填、不可为 null、描述：维护者列表；每项含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：[]。
  - 当前版本 api_categories：array 类型，必填、不可为 null、描述：API 分类；每项含 id:int、service_id:int、name:string、description:string|null、示例值：[]。
  - 当前版本 apis：array 类型，必填、不可为 null、描述：正式 API；每项含 id:int、service_id:int、owner_id:int、category_id:int|null、name:string、method:string、path:string、description:string|null、level:string、is_enabled:boolean、created_at:string(date-time)、updated_at:string(date-time)、示例值：[]。
  - 当前版本 iterations：array 类型，必填、不可为 null、描述：迭代记录；每项含 id:int、service_id:int、creator_id:int|null、version:string|null、description:string|null、created_at:string(date-time)、is_committed:boolean、示例值：[]。
  - 历史版本 id：int 类型，必填、不可为 null、描述：迭代 ID、示例值：301。
  - 历史版本 service_id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - 历史版本 creator_id：int 类型，可为 null、描述：迭代创建者 ID、示例值：1。
  - 历史版本 version：string 类型，可为 null、描述：历史版本号、示例值：0.0.1。
  - 历史版本 description：string 类型，可为 null、描述：历史说明、示例值：订单服务。
  - 历史版本 created_at：string 类型，必填、不可为 null、描述：迭代创建时间、示例值：2026-09-02T10:00:00。
  - 历史版本 is_committed：boolean 类型，必填、不可为 null、描述：是否已发布、示例值：true。
  - 历史版本 creator：object 类型，必填、不可为 null、描述：迭代创建者，含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"}。
  - 历史版本 api_drafts：array 类型，必填、不可为 null、描述：草稿 API 列表、示例值：[]。

请求示例：

GET /v1/service/getServiceByUuidAndVersion?service_uuid=order-service&version=1.0.0

响应值示例：

{"status":200,"message":"Get service success","is_latest":true,"service":{"id":101,"owner_id":1,"service_uuid":"order-service","version":"1.0.0","description":"订单服务","is_deleted":false,"apis":[]}}

## GetAllVersionsByUuid

- API 名称：GetAllVersionsByUuid
- 请求方法与路径：GET /v1/service/getAllVersionsByUuid
- 接口等级：P2
- 接口描述：查询服务当前及历史版本列表。
- 请求参数：
  - Query 参数：
    - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get service versions success。
    - versions：array 类型，必填、不可为 null、描述：版本列表、示例值：见响应示例。
- versions 元素类型：
  - version：string 类型，可为 null、描述：版本号、示例值：1.0.0。
  - is_latest：boolean 类型，必填、不可为 null、描述：是否当前版本、示例值：true。

请求示例：

GET /v1/service/getAllVersionsByUuid?service_uuid=order-service

响应值示例：

{"status":200,"message":"Get service versions success","versions":[{"version":"1.0.0","is_latest":true},{"version":"0.0.1","is_latest":false}]}

## CreateNewService

- API 名称：CreateNewService
- 请求方法与路径：POST /v1/service/createNewService
- 接口等级：P1
- 接口描述：以当前用户为所有者创建服务，初始版本固定为 0.0.1。
- 请求参数：
  - Body 参数：
    - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
    - description：string 类型，必填、不可为 null、描述：服务说明、示例值：订单服务。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Create service success。
    - service：object 类型，必填、不可为 null、描述：新建服务详情、示例值：见响应示例。
- service 类型：
  - id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - owner_id：int 类型，必填、不可为 null、描述：服务所有者 ID、示例值：1。
  - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
  - version：string 类型，必填、不可为 null、描述：初始版本、示例值：0.0.1。
  - description：string 类型，可为 null、描述：服务说明、示例值：订单服务。
  - created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - updated_at：string 类型，必填、不可为 null、描述：更新时间、示例值：2026-09-02T10:00:00。
  - is_deleted：boolean 类型，必填、不可为 null、描述：是否软删除、示例值：false。
  - deleted_at：string 类型，可为 null、描述：删除时间、示例值：null。
  - owner：object 类型，必填、不可为 null、描述：所有者，含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"}。
  - maintainers：array 类型，必填、不可为 null、描述：维护者列表；每项含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：[]。
  - api_categories：array 类型，必填、不可为 null、描述：分类列表；每项含 id:int、service_id:int、name:string、description:string|null、示例值：[]。
  - apis：array 类型，必填、不可为 null、描述：API 列表；每项含 id:int、service_id:int、owner_id:int、category_id:int|null、name:string、method:string、path:string、description:string|null、level:string、is_enabled:boolean、created_at:string(date-time)、updated_at:string(date-time)、示例值：[]。
  - iterations：array 类型，必填、不可为 null、描述：迭代列表；每项含 id:int、service_id:int、creator_id:int|null、version:string|null、description:string|null、created_at:string(date-time)、is_committed:boolean、示例值：[]。

请求示例：

{"service_uuid":"order-service","description":"订单服务"}

响应值示例：

{"status":200,"message":"Create service success","service":{"id":101,"owner_id":1,"service_uuid":"order-service","version":"0.0.1","description":"订单服务","is_deleted":false,"maintainers":[],"api_categories":[],"apis":[],"iterations":[]}}

## GetAllDeletedServicesByUserId

- API 名称：GetAllDeletedServicesByUserId
- 请求方法与路径：GET /v1/service/getAllDeletedServicesByUserId
- 接口等级：P2
- 接口描述：分页查询当前用户已软删除服务。
- 请求参数：
  - Query 参数：
    - page_size：int 类型，可选、不可为 null、描述：每页数量，默认值：10、示例值：10。
    - current_page：int 类型，可选、不可为 null、描述：页码，默认值：1、示例值：1。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get deleted services success。
    - deleted_services：array 类型，必填、不可为 null、描述：已删除服务列表、示例值：见响应示例。
    - total：int 类型，必填、不可为 null、描述：已删除服务总数、示例值：1。
- deleted_services 元素类型：
  - id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
  - description：string 类型，可为 null、描述：服务说明、示例值：订单服务。
  - version：string 类型，必填、不可为 null、描述：服务版本、示例值：1.0.0。
  - owner_id：int 类型，必填、不可为 null、描述：所有者 ID、示例值：1。
  - created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - is_deleted：boolean 类型，必填、不可为 null、描述：是否软删除、示例值：true。
  - deleted_at：string 类型，可为 null、描述：删除时间、示例值：2026-09-02T11:00:00。

请求示例：

GET /v1/service/getAllDeletedServicesByUserId?page_size=10&current_page=1

响应值示例：

{"status":200,"message":"Get deleted services success","deleted_services":[{"id":101,"service_uuid":"order-service","description":"订单服务","version":"1.0.0","owner_id":1,"created_at":"2026-09-02T10:00:00","is_deleted":true,"deleted_at":"2026-09-02T11:00:00"}],"total":1}

## IsServiceMaintainer

- API 名称：IsServiceMaintainer
- 请求方法与路径：GET /v1/service/isServiceMaintainer
- 接口等级：P2
- 接口描述：判断候选用户是否为指定服务维护者。
- 请求参数：
  - Query 参数：
    - service_id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
    - candidate_id：int 类型，必填、不可为 null、描述：候选用户 ID、示例值：2。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Check service maintainer success。
    - is_current_maintainer：boolean 类型，必填、不可为 null、描述：候选用户是否为维护者、示例值：true。

请求示例：

GET /v1/service/isServiceMaintainer?service_id=101&candidate_id=2

响应值示例：

{"status":200,"message":"Check service maintainer success","is_current_maintainer":true}

## AddOrRemoveServiceMaintainerById

- API 名称：AddOrRemoveServiceMaintainerById
- 请求方法与路径：POST /v1/service/addOrRemoveServiceMaintainerById
- 接口等级：P1
- 接口描述：添加或移除维护者；候选用户已是维护者时移除，否则添加。
- 请求参数：
  - Body 参数：
    - service_id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
    - candidate_id：int 类型，必填、不可为 null、描述：候选用户 ID、示例值：2。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Add service maintainer success。
    - is_current_maintainer：boolean 类型，必填、不可为 null、描述：切换后的维护者状态、示例值：true。

请求示例：

{"service_id":101,"candidate_id":2}

响应值示例：

{"status":200,"message":"Add service maintainer success","is_current_maintainer":true}

## DeleteServiceById

- API 名称：DeleteServiceById
- 请求方法与路径：POST /v1/service/deleteServiceById
- 接口等级：P1
- 接口描述：软删除指定服务的当前版本，历史迭代不删除。
- 请求参数：
  - Body 参数：
    - id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Delete service success。

请求示例：

{"id":101}

响应值示例：

{"status":200,"message":"Delete service success"}

## RestoreServiceById

- API 名称：RestoreServiceById
- 请求方法与路径：POST /v1/service/restoreServiceById
- 接口等级：P1
- 接口描述：恢复指定的已软删除服务。
- 请求参数：
  - Body 参数：
    - id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Restore service success。

请求示例：

{"id":101}

响应值示例：

{"status":200,"message":"Restore service success"}

## DeleteIterationById

- API 名称：DeleteIterationById
- 请求方法与路径：POST /v1/service/deleteIterationById
- 接口等级：P1
- 接口描述：删除指定历史或草稿迭代，以及该迭代下的草稿 API 和参数。
- 请求参数：
  - Body 参数：
    - service_iteration_id：int 类型，必填、不可为 null、描述：服务迭代 ID、示例值：301。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Delete service iteration success。

请求示例：

{"service_iteration_id":301}

响应值示例：

{"status":200,"message":"Delete service iteration success"}

## DeleteServicePermanentlyById

- API 名称：DeleteServicePermanentlyById
- 请求方法与路径：POST /v1/service/deleteServicePermanentlyById
- 接口等级：P0
- 接口描述：永久删除已软删除服务、全部正式 API、全部迭代、草稿 API 和关联参数。
- 请求参数：
  - Body 参数：
    - id：int 类型，必填、不可为 null、描述：已软删除服务 ID、示例值：101。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Delete service success。

请求示例：

{"id":101}

响应值示例：

{"status":200,"message":"Delete service success"}

## GetIterationById

- API 名称：GetIterationById
- 请求方法与路径：GET /v1/service/getIterationById
- 接口等级：P2
- 接口描述：查询未提交服务迭代的完整草稿信息；迭代已提交时返回业务错误。
- 请求参数：
  - Query 参数：
    - id：int 类型，必填、不可为 null、描述：服务迭代 ID、示例值：301。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get service iteration success。
    - iteration：object 类型，必填、不可为 null、描述：服务迭代详情、示例值：见响应示例。
- iteration 类型：
  - id：int 类型，必填、不可为 null、描述：迭代 ID、示例值：301。
  - service_id：int 类型，必填、不可为 null、描述：所属服务 ID、示例值：101。
  - creator_id：int 类型，可为 null、描述：迭代创建者 ID、示例值：1。
  - version：string 类型，可为 null、描述：提交后的版本号，未提交时为 null、示例值：null。
  - description：string 类型，可为 null、描述：草稿服务说明、示例值：订单服务 V2。
  - created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - is_committed：boolean 类型，必填、不可为 null、描述：是否已提交、示例值：false。
  - service：object 类型，必填、不可为 null、描述：关联服务，含 id:int、owner_id:int、service_uuid:string、version:string、description:string|null、created_at:string(date-time)、updated_at:string(date-time)、is_deleted:boolean、deleted_at:string(date-time)|null、示例值：{"id":101,"owner_id":1,"service_uuid":"order-service","version":"1.0.0","description":"订单服务","is_deleted":false,"deleted_at":null}。
  - creator：object 类型，必填、不可为 null、描述：创建者，含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"}。
  - api_drafts：array 类型，必填、不可为 null、描述：草稿 API 列表、示例值：[]。

请求示例：

GET /v1/service/getIterationById?id=301

响应值示例：

{"status":200,"message":"Get service iteration success","iteration":{"id":301,"service_id":101,"creator_id":1,"version":null,"description":"订单服务 V2","created_at":"2026-09-02T10:00:00","is_committed":false,"api_drafts":[]}}

## StartIteration

- API 名称：StartIteration
- 请求方法与路径：POST /v1/service/startIteration
- 接口等级：P1
- 接口描述：发起服务迭代，并将当前正式 API 与参数复制为草稿；当前用户已有未提交迭代时直接返回已有迭代 ID。
- 请求参数：
  - Body 参数：
    - service_id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：新建迭代时的业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Start service iteration success。
    - service_iteration_id：int 类型，必填、不可为 null、描述：新建或已有的迭代 ID、示例值：301。
  - 201：
    - status：int 类型，必填、不可为 null、描述：存在未提交迭代时的业务状态码、示例值：201。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：You have an uncommitted service iteration in progress。
    - service_iteration_id：int 类型，必填、不可为 null、描述：已有迭代 ID、示例值：301。

请求示例：

{"service_id":101}

响应值示例：

{"status":200,"message":"Start service iteration success","service_iteration_id":301}

## CommitIteration

- API 名称：CommitIteration
- 请求方法与路径：POST /v1/service/commitIteration
- 接口等级：P0
- 接口描述：提交草稿迭代，将草稿服务描述、API 和参数发布为当前正式版本。
- 请求参数：
  - Body 参数：
    - service_iteration_id：int 类型，必填、不可为 null、描述：待提交迭代 ID、示例值：301。
    - new_version：string 类型，必填、不可为 null、描述：新服务版本，不能等于当前版本、示例值：1.1.0。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Commit service iteration success。
    - service_id：int 类型，必填、不可为 null、描述：正式服务 ID、示例值：101。
    - service_iteration_id：int 类型，必填、不可为 null、描述：已提交迭代 ID、示例值：301。
    - version：string 类型，必填、不可为 null、描述：已发布版本、示例值：1.1.0。

请求示例：

{"service_iteration_id":301,"new_version":"1.1.0"}

响应值示例：

{"status":200,"message":"Commit service iteration success","service_id":101,"service_iteration_id":301,"version":"1.1.0"}

## UpdateDescription

- API 名称：UpdateDescription
- 请求方法与路径：POST /v1/service/updateDescription
- 接口等级：P2
- 接口描述：更新未提交服务迭代的服务描述。
- 请求参数：
  - Body 参数：
    - service_iteration_id：int 类型，必填、不可为 null、描述：服务迭代 ID、示例值：301。
    - description：string 类型，必填、不可为 null、描述：更新后的服务描述、示例值：订单服务 V2。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Update service description success。

请求示例：

{"service_iteration_id":301,"description":"订单服务 V2"}

响应值示例：

{"status":200,"message":"Update service description success"}

## ImportOpenapi

- API 名称：ImportOpenapi
- 请求方法与路径：POST /v1/service/importOpenapi
- 接口等级：P1
- 接口描述：为现有服务创建空的未提交迭代，并将 OpenAPI 3.0.x 或 3.1.x JSON 文档导入为 API 与参数草稿。当前用户已有未提交迭代时拒绝导入；导入过程为单事务，失败时不保留部分数据。
- 请求参数：
  - Body 参数：
    - service_id：int 类型，必填、不可为 null、描述：目标服务 ID、示例值：101。
    - openapi_object：object 类型，必填、不可为 null、描述：待导入的 OpenAPI JSON 文档、示例值：见请求示例。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Import OpenAPI success。
    - service_iteration_id：int 类型，必填、不可为 null、描述：新建的导入迭代 ID、示例值：301。
    - api_count：int 类型，必填、不可为 null、描述：导入的 API 数量、示例值：1。
    - request_param_count：int 类型，必填、不可为 null、描述：导入的请求参数总数（含嵌套参数）、示例值：1。
    - response_param_count：int 类型，必填、不可为 null、描述：导入的响应参数总数（含嵌套参数）、示例值：1。
    - warnings：array 类型，必填、不可为 null、描述：未阻断导入的兼容性提示、示例值：[]。

请求示例：

```json
{
  "service_id": 101,
  "openapi_object": {
    "openapi": "3.1.0",
    "info": {"title": "order-service", "version": "2.0.0"},
    "paths": {
      "/orders/{id}": {
        "get": {
          "operationId": "getOrder",
          "parameters": [
            {"name": "id", "in": "path", "required": true, "schema": {"type": "integer"}}
          ],
          "responses": {
            "200": {
              "description": "OK",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {"id": {"type": "integer"}},
                    "required": ["id"]
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

响应值示例：

```json
{"status":200,"message":"Import OpenAPI success","service_iteration_id":301,"api_count":1,"request_param_count":1,"response_param_count":1,"warnings":[]}
```

兼容性说明：

- 接受 JSON 格式的 OpenAPI 3.0.x 和 3.1.x 文档。
- 支持 GET、POST、PUT、DELETE 和 PATCH；其他 HTTP 方法会跳过并产生 warning。
- 支持本地 `$ref`、JSON 请求体、JSON 响应体以及 query、path、header、cookie 参数。
- `allOf`、`oneOf`、`anyOf`、递归或外部 `$ref` 等 CAM 无法无损表达的结构会拒绝导入。
- 非 JSON content、无响应体及非整数响应码会跳过，并通过 `warnings` 返回提示。
- 导入后的 API 默认等级为 P2、分类为空；`deprecated: true` 会映射为停用状态。

## ExportOpenapiByUuidAndVersion

- API 名称：ExportOpenapiByUuidAndVersion
- 请求方法与路径：GET /v1/service/exportOpenapiByUuidAndVersion
- 接口等级：P2
- 接口描述：按服务 UUID 和版本导出 OpenAPI 3.1.0 文档对象；version 为 latest 时导出当前版本。
- 请求参数：
  - Query 参数：
    - service_uuid：string 类型，必填、不可为 null、描述：服务唯一标识、示例值：order-service。
    - version：string 类型，必填、不可为 null、描述：服务版本或 latest、示例值：1.0.0。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get service success。
    - openapi_object：object 类型，必填、不可为 null、描述：OpenAPI 3.1.0 文档、示例值：见响应示例。
    - is_latest：boolean 类型，必填、不可为 null、描述：是否当前版本、示例值：true。
- openapi_object 类型：
  - openapi：string 类型，必填、不可为 null、描述：OpenAPI 规范版本、示例值：3.1.0。
  - info：object 类型，必填、不可为 null、描述：文档基础信息、示例值：见响应示例。
  - paths：object 类型，必填、不可为 null、描述：路径定义、示例值：{}。
  - components：object 类型，必填、不可为 null、描述：可复用组件、示例值：{"schemas":{}}。
- info 类型：
  - title：string 类型，必填、不可为 null、描述：服务名称、示例值：order-service。
  - description：string 类型，可为 null、描述：服务说明、示例值：订单服务。
  - version：string 类型，必填、不可为 null、描述：文档版本、示例值：1.0.0。
  - contact：object 类型，可为 null、描述：联系人信息、示例值：{"name":"alice","email":"alice@example.com"}。

请求示例：

GET /v1/service/exportOpenapiByUuidAndVersion?service_uuid=order-service&version=1.0.0

响应值示例：

{"status":200,"message":"Get service success","is_latest":true,"openapi_object":{"openapi":"3.1.0","info":{"title":"order-service","description":"订单服务","version":"1.0.0"},"paths":{},"components":{"schemas":{}}}}

# API SubRouter API

## GetAllCategoriesByServiceId

- API 名称：GetAllCategoriesByServiceId
- 请求方法与路径：GET /v1/api/getAllCategoriesByServiceId
- 接口等级：P2
- 接口描述：查询指定服务下的全部 API 分类。
- 请求参数：
  - Query 参数：
    - service_id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get all categories success。
    - categories：array 类型，必填、不可为 null、描述：API 分类列表、示例值：见响应值示例。
- categories 元素类型：
  - id：int 类型，必填、不可为 null、描述：分类 ID、示例值：10。
  - service_id：int 类型，必填、不可为 null、描述：所属服务 ID、示例值：101。
  - name：string 类型，必填、不可为 null、描述：分类名称、示例值：用户。
  - description：string 类型，可为 null、描述：分类说明、示例值：用户相关接口。

请求示例：

GET /v1/api/getAllCategoriesByServiceId?service_id=101

响应值示例：

{"status":200,"message":"Get all categories success","categories":[{"id":10,"service_id":101,"name":"用户","description":"用户相关接口"}]}

## GetAllApisByServiceId

- API 名称：GetAllApisByServiceId
- 请求方法与路径：GET /v1/api/getAllApisByServiceId
- 接口等级：P2
- 接口描述：按服务查询最新正式 API 简表，可通过分类筛选，不返回请求和响应参数。
- 请求参数：
  - Query 参数：
    - service_id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
    - category_id：int 类型，选填、不可为 null、描述：API 分类 ID；不传时返回服务下全部 API、示例值：10。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get all apis success。
    - apis：array 类型，必填、不可为 null、描述：正式 API 列表、示例值：见响应值示例。
- apis 元素类型：
  - id：int 类型，必填、不可为 null、描述：API ID、示例值：501。
  - service_id：int 类型，必填、不可为 null、描述：所属服务 ID、示例值：101。
  - owner_id：int 类型，必填、不可为 null、描述：API 创建者 ID、示例值：1。
  - category_id：int 类型，可为 null、描述：所属分类 ID、示例值：10。
  - name：string 类型，必填、不可为 null、描述：API 名称、示例值：getUser。
  - method：string 类型，必填、不可为 null、描述：HTTP 方法，枚举 GET、POST、PUT、DELETE、PATCH、示例值：GET。
  - path：string 类型，必填、不可为 null、描述：API 路径、示例值：/v1/user/{id}。
  - description：string 类型，可为 null、描述：API 描述、示例值：获取用户。
  - level：string 类型，必填、不可为 null、描述：API 等级，枚举 P0、P1、P2、P3、P4、示例值：P2。
  - is_enabled：boolean 类型，必填、不可为 null、描述：是否启用、示例值：true。
  - created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - updated_at：string 类型，必填、不可为 null、描述：更新时间、示例值：2026-09-02T10:00:00。

请求示例：

GET /v1/api/getAllApisByServiceId?service_id=101

响应值示例：

{"status":200,"message":"Get all apis success","apis":[{"id":501,"service_id":101,"owner_id":1,"category_id":10,"name":"getUser","method":"GET","path":"/v1/user/{id}","description":"获取用户","level":"P2","is_enabled":true,"created_at":"2026-09-02T10:00:00","updated_at":"2026-09-02T10:00:00"}]}

## GetApiById

- API 名称：GetApiById
- 请求方法与路径：GET /v1/api/getApiById
- 接口等级：P2
- 接口描述：查询正式 API 或草稿 API 的完整详情；请求参数按位置分组，响应参数按 HTTP 状态码分组。
- 请求参数：
  - Query 参数：
    - api_id：int 类型，必填、不可为 null、描述：正式 API ID 或草稿 API ID、示例值：501。
    - is_latest：boolean 类型，可选、不可为 null、描述：是否查询正式 API，默认值：true；false 时 api_id 表示草稿 API ID、示例值：true。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get api success。
    - api：object 类型，必填、不可为 null、描述：API 详情、示例值：见响应值示例。
- api 类型：
  - id：int 类型，必填、不可为 null、描述：API ID、示例值：501。
  - service_id：int 类型，is_latest 为 true 时必填、不可为 null、描述：所属服务 ID、示例值：101。
  - service_iteration_id：int 类型，is_latest 为 false 时必填、不可为 null、描述：所属服务迭代 ID、示例值：301。
  - owner_id：int 类型，必填、不可为 null、描述：API 所有者 ID、示例值：1。
  - category_id：int 类型，可为 null、描述：分类 ID、示例值：10。
  - name：string 类型，必填、不可为 null、描述：API 名称、示例值：getUser。
  - method：string 类型，必填、不可为 null、描述：HTTP 方法、示例值：GET。
  - path：string 类型，必填、不可为 null、描述：API 路径、示例值：/v1/user/{id}。
  - description：string 类型，可为 null、描述：API 描述、示例值：获取用户。
  - level：string 类型，必填、不可为 null、描述：API 等级、示例值：P2。
  - is_enabled：boolean 类型，必填、不可为 null、描述：是否启用、示例值：true。
  - created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - updated_at：string 类型，必填、不可为 null、描述：更新时间、示例值：2026-09-02T10:00:00。
  - owner：object 类型，必填、不可为 null、描述：API 所有者，含 id:int、username:string、nickname:string|null、email:string|null、role:string、level:int、created_at:string(date-time)、示例值：{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00"}。
  - request_params_by_location：object 类型，必填、不可为 null、描述：按 query、path、header、cookie、body 分组的请求参数、示例值：见响应值示例。
  - response_params_by_status_code：object 类型，必填、不可为 null、描述：按状态码字符串分组的响应参数、示例值：见响应值示例。
- request_params_by_location 元素类型：
  - id：int 类型，必填、不可为 null、描述：请求参数 ID、示例值：1。
  - api_id：int 类型，正式 API 时必填、不可为 null、描述：所属正式 API ID、示例值：501。
  - api_draft_id：int 类型，草稿 API 时必填、不可为 null、描述：所属草稿 API ID、示例值：601。
  - name：string 类型，必填、不可为 null、描述：参数名称、示例值：id。
  - location：string 类型，必填、不可为 null、描述：参数位置，枚举 query、path、header、cookie、body、示例值：path。
  - type：string 类型，必填、不可为 null、描述：参数类型，枚举 string、int、double、boolean、array、object、binary、示例值：int。
  - required：boolean 类型，必填、不可为 null、描述：是否必填、示例值：true。
  - nullable：boolean 类型，必填、不可为 null、描述：是否允许 JSON null、示例值：false。
  - default_value：string 类型，可为 null、描述：默认值、示例值：null。
  - description：string 类型，可为 null、描述：参数说明、示例值：用户 ID。
  - example：string 类型，可为 null、描述：参数示例、示例值：1。
  - array_child_type：string 类型，可为 null、描述：数组元素类型、示例值：null。
  - parent_param_id：int 类型，可为 null、描述：父参数 ID、示例值：null。
  - children_params：array 类型，可为 null、描述：对象或对象数组的子参数、示例值：[]。
- response_params_by_status_code 元素类型：
  - id：int 类型，必填、不可为 null、描述：响应参数 ID、示例值：2。
  - api_id：int 类型，正式 API 时必填、不可为 null、描述：所属正式 API ID、示例值：501。
  - api_draft_id：int 类型，草稿 API 时必填、不可为 null、描述：所属草稿 API ID、示例值：601。
  - status_code：int 类型，必填、不可为 null、描述：HTTP 响应状态码、示例值：200。
  - name：string 类型，必填、不可为 null、描述：响应字段名称、示例值：id。
  - type：string 类型，必填、不可为 null、描述：响应字段类型，枚举 string、int、double、boolean、array、object、binary、示例值：int。
  - required：boolean 类型，必填、不可为 null、描述：是否必填、示例值：true。
  - nullable：boolean 类型，必填、不可为 null、描述：是否允许 JSON null、示例值：false。
  - description：string 类型，可为 null、描述：字段说明、示例值：用户 ID。
  - example：string 类型，可为 null、描述：字段示例、示例值：1。
  - array_child_type：string 类型，可为 null、描述：数组元素类型、示例值：null。
  - parent_param_id：int 类型，可为 null、描述：父字段 ID、示例值：null。
  - children_params：array 类型，可为 null、描述：对象或对象数组子字段、示例值：[]。

请求示例：

GET /v1/api/getApiById?api_id=501&is_latest=true

响应值示例：

{"status":200,"message":"Get api success","api":{"id":501,"service_id":101,"owner_id":1,"category_id":10,"name":"getUser","method":"GET","path":"/v1/user/{id}","description":"获取用户","level":"P2","is_enabled":true,"request_params_by_location":{"query":[],"path":[{"id":1,"api_id":501,"name":"id","location":"path","type":"int","required":true,"nullable":false,"default_value":null,"description":"用户 ID","example":"1","array_child_type":null,"parent_param_id":null}],"header":[],"cookie":[],"body":[]},"response_params_by_status_code":{"200":[{"id":2,"api_id":501,"status_code":200,"name":"id","type":"int","required":true,"nullable":false,"description":"用户 ID","example":"1","array_child_type":null,"parent_param_id":null}]}}}

## AddCategoryByServiceId

- API 名称：AddCategoryByServiceId
- 请求方法与路径：POST /v1/api/addCategoryByServiceId
- 接口等级：P2
- 接口描述：为指定服务新增 API 分类，同一服务下分类名称唯一。
- 请求参数：
  - Body 参数：
    - service_id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
    - category_name：string 类型，必填、不可为 null、描述：分类名称、示例值：用户。
    - description：string 类型，必填、可为 null、描述：分类说明、示例值：用户相关接口。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Add category success。
    - category：object 类型，必填、不可为 null、描述：新建分类、示例值：见响应值示例。
- category 类型：
  - id：int 类型，必填、不可为 null、描述：分类 ID、示例值：10。
  - service_id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - name：string 类型，必填、不可为 null、描述：分类名称、示例值：用户。
  - description：string 类型，可为 null、描述：分类说明、示例值：用户相关接口。

请求示例：

{"service_id":101,"category_name":"用户","description":"用户相关接口"}

响应值示例：

{"status":200,"message":"Add category success","category":{"id":10,"service_id":101,"name":"用户","description":"用户相关接口"}}

## DeleteCategoryById

- API 名称：DeleteCategoryById
- 请求方法与路径：POST /v1/api/deleteCategoryById
- 接口等级：P1
- 接口描述：删除指定 API 分类。
- 请求参数：
  - Body 参数：
    - category_id：int 类型，必填、不可为 null、描述：分类 ID、示例值：10。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Delete category success。

请求示例：

{"category_id":10}

响应值示例：

{"status":200,"message":"Delete category success"}

## UpdateCategoryById

- API 名称：UpdateCategoryById
- 请求方法与路径：POST /v1/api/updateCategoryById
- 接口等级：P2
- 接口描述：更新指定 API 分类名称和说明。
- 请求参数：
  - Body 参数：
    - category_id：int 类型，必填、不可为 null、描述：分类 ID、示例值：10。
    - category_name：string 类型，必填、可为 null、描述：更新后的分类名称、示例值：账户。
    - description：string 类型，必填、可为 null、描述：更新后的分类说明、示例值：账户相关接口。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Update category success。
    - category：object 类型，必填、不可为 null、描述：更新后的分类、示例值：见响应值示例。
- category 类型：
  - id：int 类型，必填、不可为 null、描述：分类 ID、示例值：10。
  - service_id：int 类型，必填、不可为 null、描述：服务 ID、示例值：101。
  - name：string 类型，必填、不可为 null、描述：分类名称、示例值：账户。
  - description：string 类型，可为 null、描述：分类说明、示例值：账户相关接口。

请求示例：

{"category_id":10,"category_name":"账户","description":"账户相关接口"}

响应值示例：

{"status":200,"message":"Update category success","category":{"id":10,"service_id":101,"name":"账户","description":"账户相关接口"}}

## UpdateApiCategoryById

- API 名称：UpdateApiCategoryById
- 请求方法与路径：POST /v1/api/updateApiCategoryById
- 接口等级：P2
- 接口描述：修改正式 API 所属分类；category_id 传 -1 时取消分类。
- 请求参数：
  - Body 参数：
    - api_id：int 类型，必填、不可为 null、描述：正式 API ID、示例值：501。
    - category_id：int 类型，必填、不可为 null、描述：目标分类 ID；-1 代表未分类、示例值：10。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Update api category success。

请求示例：

{"api_id":501,"category_id":10}

响应值示例：

{"status":200,"message":"Update api category success"}

## AddApi

- API 名称：AddApi
- 请求方法与路径：POST /v1/api/addApi
- 接口等级：P1
- 接口描述：在未提交的服务迭代中创建 API 草稿。
- 请求参数：
  - Body 参数：
    - service_iteration_id：int 类型，必填、不可为 null、描述：未提交服务迭代 ID、示例值：301。
    - name：string 类型，必填、不可为 null、描述：API 名称、示例值：getUser。
    - method：string 类型，必填、不可为 null、描述：HTTP 方法，枚举 GET、POST、PUT、DELETE、PATCH、示例值：GET。
    - path：string 类型，必填、不可为 null、描述：API 路径、示例值：/v1/user/{id}。
    - description：string 类型，必填、不可为 null、描述：API 描述、示例值：获取用户。
    - level：string 类型，必填、不可为 null、描述：API 等级，枚举 P0、P1、P2、P3、P4、示例值：P2。
    - category_id：int 类型，可选、可为 null、描述：API 分类 ID、示例值：10。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Add api success。
    - api：object 类型，必填、不可为 null、描述：新建 API 草稿、示例值：见响应值示例。
- api 类型：
  - id：int 类型，必填、不可为 null、描述：草稿 API ID、示例值：601。
  - service_iteration_id：int 类型，必填、不可为 null、描述：服务迭代 ID、示例值：301。
  - owner_id：int 类型，必填、不可为 null、描述：草稿创建者 ID、示例值：1。
  - category_id：int 类型，可为 null、描述：分类 ID、示例值：10。
  - name：string 类型，必填、不可为 null、描述：API 名称、示例值：getUser。
  - method：string 类型，必填、不可为 null、描述：HTTP 方法、示例值：GET。
  - path：string 类型，必填、不可为 null、描述：API 路径、示例值：/v1/user/{id}。
  - description：string 类型，可为 null、描述：API 描述、示例值：获取用户。
  - level：string 类型，必填、不可为 null、描述：API 等级、示例值：P2。
  - is_enabled：boolean 类型，必填、不可为 null、描述：是否启用、示例值：true。
  - created_at：string 类型，必填、不可为 null、描述：创建时间、示例值：2026-09-02T10:00:00。
  - updated_at：string 类型，必填、不可为 null、描述：更新时间、示例值：2026-09-02T10:00:00。

请求示例：

{"service_iteration_id":301,"name":"getUser","method":"GET","path":"/v1/user/{id}","description":"获取用户","level":"P2","category_id":10}

响应值示例：

{"status":200,"message":"Add api success","api":{"id":601,"service_iteration_id":301,"owner_id":1,"category_id":10,"name":"getUser","method":"GET","path":"/v1/user/{id}","description":"获取用户","level":"P2","is_enabled":true,"created_at":"2026-09-02T10:00:00","updated_at":"2026-09-02T10:00:00"}}

## CopyApiByApiDraftId

- API 名称：CopyApiByApiDraftId
- 请求方法与路径：POST /v1/api/copyApiByApiDraftId
- 接口等级：P2
- 接口描述：复制同一未提交迭代中的 API 草稿及其所有嵌套请求、响应参数。
- 请求参数：
  - Body 参数：
    - service_iteration_id：int 类型，必填、不可为 null、描述：服务迭代 ID、示例值：301。
    - api_draft_id：int 类型，必填、不可为 null、描述：待复制草稿 API ID、示例值：601。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Copy api success。

请求示例：

{"service_iteration_id":301,"api_draft_id":601}

响应值示例：

{"status":200,"message":"Copy api success"}

## DeleteApiByApiDraftId

- API 名称：DeleteApiByApiDraftId
- 请求方法与路径：POST /v1/api/deleteApiByApiDraftId
- 接口等级：P1
- 接口描述：删除未提交迭代中的 API 草稿及其全部请求、响应参数。
- 请求参数：
  - Body 参数：
    - service_iteration_id：int 类型，必填、不可为 null、描述：服务迭代 ID、示例值：301。
    - api_draft_id：int 类型，必填、不可为 null、描述：待删除草稿 API ID、示例值：601。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Delete api success。

请求示例：

{"service_iteration_id":301,"api_draft_id":601}

响应值示例：

{"status":200,"message":"Delete api success"}

## UpdateApiByApiDraftId

- API 名称：UpdateApiByApiDraftId
- 请求方法与路径：POST /v1/api/updateApiByApiDraftId
- 接口等级：P1
- 接口描述：覆盖更新未提交 API 草稿的基本信息，并先删除后重建其请求和响应参数树。
- 请求参数：
  - Body 参数：
    - service_iteration_id：int 类型，必填、不可为 null、描述：服务迭代 ID、示例值：301。
    - api_draft_id：int 类型，必填、不可为 null、描述：草稿 API ID、示例值：601。
    - name：string 类型，必填、不可为 null、描述：API 名称、示例值：getUser。
    - method：string 类型，必填、不可为 null、描述：HTTP 方法，枚举 GET、POST、PUT、DELETE、PATCH、示例值：GET。
    - path：string 类型，必填、不可为 null、描述：API 路径、示例值：/v1/user/{id}。
    - description：string 类型，必填、不可为 null、描述：API 描述、示例值：获取用户。
    - level：string 类型，必填、不可为 null、描述：API 等级，枚举 P0、P1、P2、P3、P4、示例值：P2。
    - req_params：string 类型，必填、不可为 null、描述：序列化后的请求参数 JSON 数组、示例值：见请求示例。
    - resp_params：string 类型，必填、不可为 null、描述：序列化后的响应参数 JSON 数组、示例值：见请求示例。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- req_params JSON 元素类型：
  - name：string 类型，必填、不可为 null、描述：参数名称、示例值：id。
  - location：string 类型，根参数必填、不可为 null、描述：参数位置，枚举 query、path、header、cookie、body；子参数不传并继承父位置、示例值：path。
  - type：string 类型，必填、不可为 null、描述：参数类型，枚举 string、int、double、boolean、array、object、binary、示例值：int。
  - required：boolean 类型，可选、不可为 null、描述：是否必填，默认值：false、示例值：true。
  - nullable：boolean 类型，可选、不可为 null、描述：是否允许 JSON null，默认值：false、示例值：false。
  - default_value：string 类型，可为 null、描述：默认值、示例值：null。
  - description：string 类型，可为 null、描述：参数说明、示例值：用户 ID。
  - example：string 类型，可为 null、描述：参数示例值、示例值：1。
  - array_child_type：string 类型，可为 null、描述：数组元素类型，枚举 string、int、double、boolean、array、object、binary、示例值：null。
  - children：array 类型，可为 null、描述：子参数；只有 type 为 object 或 type 为 array 且 array_child_type 为 object 时生效、示例值：null。
- resp_params JSON 元素类型：
  - status_code：int 类型，可选、不可为 null、描述：HTTP 响应状态码，默认值：200、示例值：200。
  - name：string 类型，必填、不可为 null、描述：响应字段名称、示例值：id。
  - type：string 类型，必填、不可为 null、描述：字段类型，枚举 string、int、double、boolean、array、object、binary、示例值：int。
  - required：boolean 类型，可选、不可为 null、描述：是否必填，默认值：false、示例值：true。
  - nullable：boolean 类型，可选、不可为 null、描述：是否允许 JSON null，默认值：false、示例值：false。
  - description：string 类型，可为 null、描述：字段说明、示例值：用户 ID。
  - example：string 类型，可为 null、描述：字段示例值、示例值：1。
  - array_child_type：string 类型，可为 null、描述：数组元素类型，枚举 string、int、double、boolean、array、object、binary、示例值：null。
  - children：array 类型，可为 null、描述：子字段；只有 type 为 object 或 type 为 array 且 array_child_type 为 object 时生效、示例值：null。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Update api success。

请求示例：

{"service_iteration_id":301,"api_draft_id":601,"name":"getUser","method":"GET","path":"/v1/user/{id}","description":"获取用户","level":"P2","req_params":"[{"name":"id","location":"path","type":"int","required":true,"nullable":false,"default_value":null,"description":"用户 ID","example":"1","array_child_type":null,"children":null}]","resp_params":"[{"status_code":200,"name":"id","type":"int","required":true,"nullable":false,"description":"用户 ID","example":"1","array_child_type":null,"children":null}]"}

响应值示例：

{"status":200,"message":"Update api success"}

# AI SubRouter API

## GenerateApiProposal

- API 名称：GenerateApiProposal
- 请求方法与路径：POST /v1/ai/generateApiProposal
- 接口等级：P2
- 接口描述：根据自然语言生成不写入数据库的 API 草案，并校验迭代权限、参数合同、重复 API 和最多八层嵌套。
- 请求参数：
  - Body 参数：
    - service_iteration_id：int 类型，必填、不可为 null、描述：未提交服务迭代 ID、示例值：301。
    - prompt：string 类型，必填、不可为 null、描述：接口需求说明；不能为空且最大长度为 8000 个字符、示例值：创建一个通过用户 ID 获取用户信息的 GET 接口，路径为 /v1/user/{id}。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200（生成成功）：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Generate API proposal success。
    - proposal：object 类型，必填、不可为 null、描述：完整 API 草案；根节点必须且只能包含 add_api、req_params、resp_params，示例值：见响应值示例。
  - 200（缺少必要信息）：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Generate API proposal success。
    - proposal：object 类型，必填、不可为 null、描述：仅含 missing_fields 字段、示例值：{"missing_fields":["method","path"]}。
  - 200（与现有 API 重复）：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Generate API proposal success。
    - proposal：object 类型，必填、不可为 null、描述：仅含 duplicate_api 和 message 字段、示例值：{"duplicate_api":{"method":"GET","path":"/v1/user/{id}"},"message":"API 已存在，不能重复创建"}。
- proposal 成功类型：
  - add_api：object 类型，必填、不可为 null、描述：API 基本信息、示例值：见响应值示例。
  - req_params：array 类型，必填、不可为 null、描述：请求参数草案、示例值：见响应值示例。
  - resp_params：array 类型，必填、不可为 null、描述：响应参数草案、示例值：见响应值示例。
- proposal 成功规则：
  - add_api：必须且只能包含 name、method、path、description、level、category_id 六个字段；name 为非空英文名称，path 必须以 / 开头。
  - req_params：每个根参数必须包含 name、location、type、required、nullable、default_value、description、example、array_child_type、children 十个字段；子参数不允许包含 location，并继承父参数位置。
  - resp_params：每个参数必须包含 status_code、name、type、required、nullable、description、example、array_child_type、children 九个字段。
  - children：只有 type 为 object 或 type 为 array 且 array_child_type 为 object 时可为数组；其他类型必须为 null。
  - path 请求参数：required 必须为 true，nullable 必须为 false。
  - 数组参数：array_child_type 为数组元素类型；当其为 object 时，children 描述每个数组元素的字段。
- proposal.add_api 类型：
  - name：string 类型，必填、不可为 null、描述：英文 API 名称、示例值：getUser。
  - method：string 类型，必填、不可为 null、描述：HTTP 方法，枚举 GET、POST、PUT、DELETE、PATCH、示例值：GET。
  - path：string 类型，必填、不可为 null、描述：API 路径，必须以 / 开头、示例值：/v1/user/{id}。
  - description：string 类型，必填、不可为 null、描述：API 描述、示例值：通过用户 ID 获取用户信息。
  - level：string 类型，必填、不可为 null、描述：API 等级，枚举 P0、P1、P2、P3、P4、示例值：P2。
  - category_id：int 类型，可为 null、描述：分类 ID、示例值：null。
- proposal.req_params 元素类型：
  - name：string 类型，必填、不可为 null、描述：参数名称、示例值：id。
  - location：string 类型，根参数必填、不可为 null、描述：参数位置，枚举 query、path、header、cookie、body、示例值：path。
  - type：string 类型，必填、不可为 null、描述：参数类型，枚举 string、int、double、boolean、array、object、binary、示例值：int。
  - required：boolean 类型，必填、不可为 null、描述：是否必填、示例值：true。
  - nullable：boolean 类型，必填、不可为 null、描述：是否允许 JSON null、示例值：false。
  - default_value：string 类型，可为 null、描述：默认值、示例值：null。
  - description：string 类型，必填、可为 null、描述：参数说明、示例值：用户 ID。
  - example：string 类型，必填、可为 null、描述：示例值、示例值：1。
  - array_child_type：string 类型，必填、可为 null、描述：数组元素类型、示例值：null。
  - children：array 类型，必填、可为 null、描述：对象或对象数组的子参数、示例值：null。
- proposal.resp_params 元素类型：
  - status_code：int 类型，必填、不可为 null、描述：HTTP 状态码，范围 100 至 599、示例值：200。
  - name：string 类型，必填、不可为 null、描述：响应字段名称、示例值：id。
  - type：string 类型，必填、不可为 null、描述：字段类型，枚举 string、int、double、boolean、array、object、binary、示例值：int。
  - required：boolean 类型，必填、不可为 null、描述：是否必填、示例值：true。
  - nullable：boolean 类型，必填、不可为 null、描述：是否允许 JSON null、示例值：false。
  - description：string 类型，必填、可为 null、描述：字段说明、示例值：用户 ID。
  - example：string 类型，必填、可为 null、描述：字段示例、示例值：1。
  - array_child_type：string 类型，必填、可为 null、描述：数组元素类型、示例值：null。
  - children：array 类型，必填、可为 null、描述：对象或对象数组的子字段、示例值：null。

请求示例：

{"service_iteration_id":301,"prompt":"创建一个通过用户 ID 获取用户信息的 GET 接口，路径为 /v1/user/{id}"}

响应值示例：

{"status":200,"message":"Generate API proposal success","proposal":{"add_api":{"name":"createOrder","method":"POST","path":"/v1/orders/{userId}","description":"为指定用户创建订单，并支持订单明细、优惠券和客户端追踪信息","level":"P1","category_id":12},"req_params":[{"name":"userId","location":"path","type":"int","required":true,"nullable":false,"default_value":null,"description":"下单用户 ID","example":"10001","array_child_type":null,"children":null},{"name":"dryRun","location":"query","type":"boolean","required":false,"nullable":false,"default_value":"false","description":"是否仅校验订单而不实际创建","example":"false","array_child_type":null,"children":null},{"name":"X-Request-Id","location":"header","type":"string","required":true,"nullable":false,"default_value":null,"description":"请求链路追踪 ID","example":"req-20260902-0001","array_child_type":null,"children":null},{"name":"sessionId","location":"cookie","type":"string","required":false,"nullable":true,"default_value":null,"description":"用户会话标识","example":"sess-abc123","array_child_type":null,"children":null},{"name":"order","location":"body","type":"object","required":true,"nullable":false,"default_value":null,"description":"订单主体","example":null,"array_child_type":null,"children":[{"name":"currency","type":"string","required":true,"nullable":false,"default_value":"CNY","description":"结算币种","example":"CNY","array_child_type":null,"children":null},{"name":"amount","type":"double","required":true,"nullable":false,"default_value":null,"description":"订单总金额","example":"199.90","array_child_type":null,"children":null},{"name":"shippingAddress","type":"object","required":true,"nullable":false,"default_value":null,"description":"收货地址","example":null,"array_child_type":null,"children":[{"name":"province","type":"string","required":true,"nullable":false,"default_value":null,"description":"省份","example":"浙江省","array_child_type":null,"children":null},{"name":"city","type":"string","required":true,"nullable":false,"default_value":null,"description":"城市","example":"杭州市","array_child_type":null,"children":null},{"name":"detail","type":"string","required":true,"nullable":false,"default_value":null,"description":"详细地址","example":"西湖区文三路 1 号","array_child_type":null,"children":null}]},{"name":"items","type":"array","required":true,"nullable":false,"default_value":null,"description":"订单商品明细","example":null,"array_child_type":"object","children":[{"name":"skuId","type":"int","required":true,"nullable":false,"default_value":null,"description":"商品 SKU ID","example":"20001","array_child_type":null,"children":null},{"name":"quantity","type":"int","required":true,"nullable":false,"default_value":"1","description":"购买数量","example":"2","array_child_type":null,"children":null},{"name":"attributes","type":"object","required":false,"nullable":true,"default_value":null,"description":"商品定制属性","example":null,"array_child_type":null,"children":[{"name":"color","type":"string","required":false,"nullable":true,"default_value":null,"description":"颜色","example":"黑色","array_child_type":null,"children":null},{"name":"size","type":"string","required":false,"nullable":true,"default_value":null,"description":"规格","example":"XL","array_child_type":null,"children":null}]}]},{"name":"couponCodes","type":"array","required":false,"nullable":false,"default_value":null,"description":"优惠券编码列表","example":"[\"NEWUSER\",\"VIP10\"]","array_child_type":"string","children":null}]}],"resp_params":[{"status_code":201,"name":"data","type":"object","required":true,"nullable":false,"description":"创建成功的订单数据","example":null,"array_child_type":null,"children":[{"name":"orderId","type":"int","required":true,"nullable":false,"description":"订单 ID","example":"900001","array_child_type":null,"children":null},{"name":"orderNo","type":"string","required":true,"nullable":false,"description":"订单编号","example":"ORD202609020001","array_child_type":null,"children":null},{"name":"totalAmount","type":"double","required":true,"nullable":false,"description":"订单总金额","example":"199.90","array_child_type":null,"children":null},{"name":"items","type":"array","required":true,"nullable":false,"description":"已创建商品明细","example":null,"array_child_type":"object","children":[{"name":"skuId","type":"int","required":true,"nullable":false,"description":"商品 SKU ID","example":"20001","array_child_type":null,"children":null},{"name":"quantity","type":"int","required":true,"nullable":false,"description":"购买数量","example":"2","array_child_type":null,"children":null},{"name":"lineAmount","type":"double","required":true,"nullable":false,"description":"商品行金额","example":"199.90","array_child_type":null,"children":null}]}]},{"status_code":400,"name":"error","type":"object","required":true,"nullable":false,"description":"参数校验失败信息","example":null,"array_child_type":null,"children":[{"name":"code","type":"string","required":true,"nullable":false,"description":"错误码","example":"INVALID_ORDER","array_child_type":null,"children":null},{"name":"message","type":"string","required":true,"nullable":false,"description":"错误说明","example":"订单商品不能为空","array_child_type":null,"children":null},{"name":"fieldErrors","type":"array","required":false,"nullable":false,"description":"字段错误列表","example":null,"array_child_type":"object","children":[{"name":"field","type":"string","required":true,"nullable":false,"description":"错误字段名","example":"order.items","array_child_type":null,"children":null},{"name":"reason","type":"string","required":true,"nullable":false,"description":"错误原因","example":"至少需要一个商品","array_child_type":null,"children":null}]}]}]}}

# User SubRouter API

## GetUserById

- API 名称：GetUserById
- 请求方法与路径：GET /v1/user/getUserById
- 接口等级：P2
- 接口描述：根据用户 ID 查询用户详细资料；仅用户等级 L0 可以调用。
- 请求参数：
  - Query 参数：
    - id：int 类型，必填、不可为 null、描述：目标用户 ID、示例值：1。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get user success。
    - user：object 类型，必填、不可为 null、描述：用户详细资料、示例值：见响应值示例。
- user 类型：
  - id：int 类型，必填、不可为 null、描述：用户 ID、示例值：1。
  - username：string 类型，必填、不可为 null、描述：用户名、示例值：alice。
  - nickname：string 类型，可为 null、描述：用户昵称、示例值：Alice。
  - email：string 类型，可为 null、描述：用户邮箱、示例值：alice@example.com。
  - role：string 类型，必填、不可为 null、描述：用户角色，枚举 frontend、backend、fullstack、qa、devops、product_manager、designer、architect、proj_lead、guest、示例值：backend。
  - level：int 类型，必填、不可为 null、描述：用户等级，L0 至 L4 分别映射为 0 至 4、示例值：0。
  - created_at：string 类型，必填、不可为 null、描述：用户创建时间（ISO 8601）、示例值：2026-09-02T10:00:00。
  - has_password：boolean 类型，必填、不可为 null、描述：是否配置本地密码、示例值：true。
  - auth_providers：array 类型，必填、不可为 null、描述：已绑定的第三方身份提供方、示例值：["google"]。

请求示例：

GET /v1/user/getUserById?id=1

响应值示例：

{"status":200,"message":"Get user success","user":{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":0,"created_at":"2026-09-02T10:00:00","has_password":true,"auth_providers":["google"]}}

## GetMyInfo

- API 名称：GetMyInfo
- 请求方法与路径：GET /v1/user/getMyInfo
- 接口等级：P1
- 接口描述：从 Bearer 访问令牌解析并查询当前登录用户资料。
- 请求参数：
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
  - Query 参数：
    - 无参数。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get user success。
    - user：object 类型，必填、不可为 null、描述：当前用户详细资料、示例值：见响应值示例。
- user 类型：
  - id：int 类型，必填、不可为 null、描述：用户 ID、示例值：1。
  - username：string 类型，必填、不可为 null、描述：用户名、示例值：alice。
  - nickname：string 类型，可为 null、描述：用户昵称、示例值：Alice。
  - email：string 类型，可为 null、描述：用户邮箱、示例值：alice@example.com。
  - role：string 类型，必填、不可为 null、描述：用户角色，枚举 frontend、backend、fullstack、qa、devops、product_manager、designer、architect、proj_lead、guest、示例值：backend。
  - level：int 类型，必填、不可为 null、描述：用户等级，L0 至 L4 分别映射为 0 至 4、示例值：4。
  - created_at：string 类型，必填、不可为 null、描述：用户创建时间（ISO 8601）、示例值：2026-09-02T10:00:00。
  - has_password：boolean 类型，必填、不可为 null、描述：是否配置本地密码、示例值：true。
  - auth_providers：array 类型，必填、不可为 null、描述：已绑定的第三方身份提供方、示例值：["google"]。

请求示例：

GET /v1/user/getMyInfo

响应值示例：

{"status":200,"message":"Get user success","user":{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00","has_password":true,"auth_providers":["google"]}}

## GetUserByUsernameOrNicknameOrEmail

- API 名称：GetUserByUsernameOrNicknameOrEmail
- 请求方法与路径：GET /v1/user/getUserByUsernameOrNicknameOrEmail
- 接口等级：P2
- 接口描述：按用户名、昵称或邮箱模糊查询用户列表。
- 请求参数：
  - Query 参数：
    - username_or_nickname_or_email：string 类型，必填、不可为 null、描述：用户名、昵称或邮箱搜索关键字、示例值：alice。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Get users success。
    - users：array 类型，必填、不可为 null、描述：匹配用户列表、示例值：见响应值示例。
- users 元素类型：
  - id：int 类型，必填、不可为 null、描述：用户 ID、示例值：1。
  - username：string 类型，必填、不可为 null、描述：用户名、示例值：alice。
  - nickname：string 类型，可为 null、描述：用户昵称、示例值：Alice。
  - email：string 类型，可为 null、描述：用户邮箱、示例值：alice@example.com。
  - role：string 类型，必填、不可为 null、描述：用户角色，枚举 frontend、backend、fullstack、qa、devops、product_manager、designer、architect、proj_lead、guest、示例值：backend。
  - level：int 类型，必填、不可为 null、描述：用户等级、示例值：4。
  - created_at：string 类型，必填、不可为 null、描述：用户创建时间（ISO 8601）、示例值：2026-09-02T10:00:00。
  - has_password：boolean 类型，必填、不可为 null、描述：是否配置本地密码、示例值：true。
  - auth_providers：array 类型，必填、不可为 null、描述：已绑定的第三方身份提供方、示例值：["google"]。

请求示例：

GET /v1/user/getUserByUsernameOrNicknameOrEmail?username_or_nickname_or_email=alice

响应值示例：

{"status":200,"message":"Get users success","users":[{"id":1,"username":"alice","nickname":"Alice","email":"alice@example.com","role":"backend","level":4,"created_at":"2026-09-02T10:00:00","has_password":true,"auth_providers":["google"]}]}

## Login

- API 名称：Login
- 请求方法与路径：POST /v1/user/login
- 接口等级：P1
- 接口描述：使用用户名或邮箱和密码登录，返回 JWT 访问令牌。
- 请求参数：
  - Body 参数：
    - username：string 类型，必填、不可为 null、描述：用户名或邮箱、示例值：alice。
    - password：string 类型，必填、不可为 null、描述：登录密码、示例值：P@ssw0rd!。
  - Header 参数：
    - 无鉴权参数。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Login success。
    - access_token：string 类型，必填、不可为 null、描述：JWT 访问令牌、示例值：eyJ...。

请求示例：

{"username":"alice","password":"P@ssw0rd!"}

响应值示例：

{"status":200,"message":"Login success","access_token":"eyJ..."}

## GoogleLogin

- API 名称：GoogleLogin
- 请求方法与路径：POST /v1/user/login/google
- 接口等级：P1
- 接口描述：校验 Google Identity Services ID Token，关联或创建 CAM 用户并返回平台 JWT。
- 请求参数：
  - Body 参数：
    - credential：string 类型，必填、不可为 null、描述：Google Identity Services 返回的 ID Token。
  - Header 参数：
    - 无鉴权参数。
- 响应参数：
  - 200：status、message、access_token，与密码登录成功响应一致。
  - 400：INVALID_REQUEST，缺少 credential。
  - 401：INVALID_GOOGLE_CREDENTIAL 或 UNVERIFIED_GOOGLE_ACCOUNT。
  - 403：GOOGLE_DOMAIN_NOT_ALLOWED。
  - 409：ACCOUNT_LINK_REQUIRED，邮箱已有本地账号，需要先密码登录后绑定。
  - 503：GOOGLE_AUTH_NOT_CONFIGURED 或 GOOGLE_AUTH_UNAVAILABLE。

请求示例：

{"credential":"<google_id_token>"}

响应值示例：

{"status":200,"message":"Login success","access_token":"eyJ..."}

## LinkGoogle

- API 名称：LinkGoogle
- 请求方法与路径：POST /v1/user/link/google
- 接口等级：P1
- 接口描述：为当前 Bearer Token 对应的 CAM 用户绑定同邮箱 Google 身份。
- 请求参数：
  - Body 参数：
    - credential：string 类型，必填、不可为 null、描述：Google Identity Services 返回的 ID Token。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌。
- 响应参数：
  - 200：status、message。
  - 409：GOOGLE_EMAIL_MISMATCH 或 GOOGLE_IDENTITY_ALREADY_LINKED。

请求示例：

{"credential":"<google_id_token>"}

响应值示例：

{"status":200,"message":"Google account linked"}

## Register

- API 名称：Register
- 请求方法与路径：POST /v1/user/register
- 接口等级：P2
- 接口描述：注册新用户。
- 请求参数：
  - Body 参数：
    - username：string 类型，必填、不可为 null、描述：用户名、示例值：alice。
    - password：string 类型，必填、不可为 null、描述：用户密码、示例值：P@ssw0rd!。
    - nickname：string 类型，必填、不可为 null、描述：用户昵称、示例值：Alice。
    - email：string 类型，必填、不可为 null、描述：用户邮箱、示例值：alice@example.com。
    - role：string 类型，必填、不可为 null、描述：用户角色，枚举 frontend、backend、fullstack、qa、devops、product_manager、designer、architect、proj_lead、guest、示例值：backend。
  - Header 参数：
    - 无鉴权参数。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Register success。

请求示例：

{"username":"alice","password":"P@ssw0rd!","nickname":"Alice","email":"alice@example.com","role":"backend"}

响应值示例：

{"status":200,"message":"Register success"}

## ModifyPassword

- API 名称：ModifyPassword
- 请求方法与路径：POST /v1/user/modifyPassword
- 接口等级：P1
- 接口描述：校验当前用户旧密码后更新密码。
- 请求参数：
  - Body 参数：
    - old_password：string 类型，必填、不可为 null、描述：当前密码、示例值：P@ssw0rd!。
    - new_password：string 类型，必填、不可为 null、描述：新密码；不能与旧密码相同、示例值：NewP@ssw0rd!。
  - Header 参数：
    - Authorization：string 类型，必填、不可为 null、描述：Bearer 访问令牌、示例值：Bearer <access_token>。
- 响应参数：
  - 200：
    - status：int 类型，必填、不可为 null、描述：业务状态码、示例值：200。
    - message：string 类型，必填、不可为 null、描述：响应信息、示例值：Modify password success。

请求示例：

{"old_password":"P@ssw0rd!","new_password":"NewP@ssw0rd!"}

响应值示例：

{"status":200,"message":"Modify password success"}

## ListUsers

- `GET /v1/user/listUsers`，需要有效 CDI Bearer Token；对所有用户角色开放。
- 全部 CDI 用户均为成员，无独立组织概念，也不按连接/同步状态筛选。
- 查询：`after_id` 默认 `0`；`limit` 默认 `100`，范围 1–100；可选 `user_id` 精确查询一个成员。
- 返回：`{"status":200,"items":[{"cdi_user_id":"1","display_name":"Alice"}],"has_more":false,"next_after_id":""}`。
- ID 是精确十进制字符串，按 ID 升序游标分页。仅返回 ID 与昵称（缺失时使用用户名），不包含邮箱、凭据或账号权限配置。无匹配成员返回空列表；非法参数返回 400；未登录使用既有认证拒绝机制。
- 供 AirJelly Team 服务端读取目录和校验资料读取对象；Team 不直连 CDI 数据库。
