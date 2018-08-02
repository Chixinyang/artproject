/*
用户表
    id
    name
    pwd
    addtime
*/
create table if not exists user (
    id int unsigned not null auto_increment key comment "主键 id",
    name varchar(20) not null comment "账号",
    pwd varchar(20) not null comment "密码",
    addtime datetime not null comment "注册时间"
)engine=InnoDB default charset=utf8 comment "用户";

//支持事务处理