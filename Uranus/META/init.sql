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
