-- Author: kahsolt
-- Date: 2017-06-25
-- Principle: Maintain tables as least as possible!

-- Database
CREATE DATABASE IF NOT EXISTS uranus CHARSET utf8mb4;
USE uranus;

-- User
CREATE USER 'uranus'@'%' IDENTIFIED BY 'uranus';	-- allow from all hosts, easy to debug
GRANT ALL PRIVILEGES ON uranus.* TO 'uranus'@'%';
FLUSH PRIVILEGES;

CREATE TABLE user (
	id INT PRIMARY KEY COMMENT '学号/工号', -- we rely on this: id==SID/ID!
	cid INT COMMENT '班号',
	username VARCHAR(32) NOT NULL,
	password VARCHAR(64) NOT NULL,
	role ENUM('学生', '教师', '教务') DEFAULT '学生' COMMENT '登录角色',
	name VARCHAR(32) NOT NULL COMMENT '实名',
	gender ENUM('男', '女') DEFAULT '男',
  tel CHAR(11) COMMENT '电话',
	email VARCHAR(64)
) CHARSET utf8 COMMENT '[用户:学生/教师/教务账户]';

CREATE TABLE term (
	id INT PRIMARY KEY AUTO_INCREMENT,
	info TEXT COMMENT '说明性信息',
	year INT,
	semester ENUM('春', '秋'),
	starttime DATETIME,
	endtime DATETIME
	-- TODO: 周次安排？！！
) CHARSET utf8 COMMENT '[学期]';

CREATE TABLE course (
	id INT PRIMARY KEY AUTO_INCREMENT,
	tid INT REFERENCES term(id) COMMENT '所属学期',
	tmid INT REFERENCES teammeta(id) COMMENT '团队元信息',
	name VARCHAR(64) NOT NULL,
	info TEXT COMMENT '课程要求/其他说明',
	syllabus TEXT COMMENT '课程大纲',
	classroom VARCHAR(128) COMMENT '上课地点',
	credit INT DEFAULT 0,
	status ENUM('未开始', '正在进行', '已结束'),
	starttime TIMESTAMP,
	endtime TIMESTAMP
) CHARSET utf8 COMMENT '[课程]==[学期]&[团队元信息]';

CREATE TABLE enroll (
	id INT PRIMARY KEY AUTO_INCREMENT,
	cid INT REFERENCES course(id),
	uid INT REFERENCES user(id)
) CHARSET utf8 COMMENT '<选课>==[课程]&[用户:学生/教师账户]';

CREATE TABLE teammeta (
	id INT PRIMARY KEY AUTO_INCREMENT,
	minnum INT DEFAULT 1,	-- mim members number
	maxnum INT DEFAULT 10,
	starttime TIMESTAMP COMMENT '允许组队的起始时间',
	endtime TIMESTAMP
) CHARSET utf8 COMMENT '[团队元信息]';;

CREATE TABLE team (
	id INT PRIMARY KEY AUTO_INCREMENT,
	cid INT REFERENCES course(id) COMMENT '所属课程',
	name VARCHAR(32) COMMENT '取代ID的备用策略',
	status ENUM('未审核', '待审核', '已通过', '已驳回'),
	info TEXT COMMENT '通过欢迎信息/驳回理由'
) CHARSET utf8 COMMENT '[团队]==[课程]&[用户:学生账户]';

CREATE TABLE member (
	id INT PRIMARY KEY AUTO_INCREMENT,
	tid INT REFERENCES team(id),
	uid INT REFERENCES user(id),
	role ENUM('队长', '队员') DEFAULT '队员',
	contribution FLOAT DEFAULT 0 COMMENT '成员贡献度:0.4~1.2'
) CHARSET utf8 COMMENT '<团队成员>==[团队]&[用户:学生账户]';

CREATE TABLE workmeta (
	id INT PRIMARY KEY AUTO_INCREMENT,
	uid INT REFERENCES user(id) COMMENT '发布者:教师',
	content TEXT,	-- plain-text
	proportion FLOAT COMMENT '总分折算占比:0.0~1.0',
	submits INT DEFAULT -1 COMMENT '可提交次数，默认-1为无限',
	starttime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	endtime TIMESTAMP
) CHARSET utf8 COMMENT '[作业任务]~~<附件>';

CREATE TABLE work (
	id INT PRIMARY KEY AUTO_INCREMENT,
	wmid INT REFERENCES workmeta(id) COMMENT '作业任务元信息',
	tid INT REFERENCES team(id) COMMENT '提交者:团队',
	content TEXT, -- plain-text
	review TEXT COMMENT '教师简评',
	score FLOAT COMMENT '得分: 0.0~10.0'
) CHARSET utf8 COMMENT '[作业提交]~~<附件>';

CREATE TABLE attachment (
	id INT PRIMARY KEY AUTO_INCREMENT,
	fid INT REFERENCES file(id),
	wmid INT REFERENCES workmeta(id),	-- whether wid/wmid works depends on 'type'
	wid INT REFERENCES work(id),
	type ENUM('作业任务', '作业提交') NOT NULL
) CHARSET utf8 COMMENT '<附件>==[作业任务|作业提交]&[资源文件]';

CREATE TABLE file (
	id INT PRIMARY KEY AUTO_INCREMENT,
	uid INT REFERENCES user(id) COMMENT '上传者',
	filename VARCHAR(256) NOT NULL COMMENT '上传时原文件名',
	path VARCHAR(512) NOT NULL COMMENT '存档时UUID名',
	type ENUM('文本', '文档', '视频')		-- should be more specific?
) CHARSET utf8 COMMENT '[资源文件]';

CREATE TABLE log (
	id INT PRIMARY KEY AUTO_INCREMENT,
	uid INT REFERENCES user(id) COMMENT '操作员',
	event TEXT COMMENT '日志记录',
	time TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
) CHARSET utf8 COMMENT '[日志]';