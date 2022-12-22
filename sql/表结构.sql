-- Adminer 4.6.3 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';


DROP TABLE IF EXISTS `movie_collectmoviedb`;
CREATE TABLE `movie_collectmoviedb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) NOT NULL COMMENT '电影唯一标识',
  `original_title` varchar(1000) NOT NULL COMMENT '原始名称',
  `title` varchar(1000) NOT NULL COMMENT '电影名称',
  `rating` longtext NOT NULL COMMENT '评分数据',
  `ratings_count` int(11) NOT NULL COMMENT '评分人数',
  `pubdate` varchar(1000) NOT NULL COMMENT '上映日期',
  `pubdates` varchar(1000) NOT NULL COMMENT '上映日期数据',
  `year` int(11) NOT NULL COMMENT '上映年份',
  `countries` varchar(1000) NOT NULL COMMENT '出版国家',
  `mainland_pubdate` varchar(1000) NOT NULL COMMENT '主要上映日期',
  `aka` varchar(1000) NOT NULL COMMENT '又名',
  `tags` varchar(1000) NOT NULL COMMENT '标签',
  `durations` longtext NOT NULL COMMENT '时长',
  `genres` varchar(1000) NOT NULL COMMENT '类型',
  `videos` longtext NOT NULL COMMENT '视频数据',
  `wish_count` int(11) NOT NULL COMMENT '想看人数',
  `reviews_count` int(11) NOT NULL COMMENT '长评人数',
  `comments_count` int(11) NOT NULL COMMENT '短评人数',
  `collect_count` int(11) NOT NULL COMMENT '收藏人数',
  `images` longtext NOT NULL COMMENT '海报数据',
  `photos` longtext NOT NULL COMMENT '图像数据',
  `languages` varchar(1000) NOT NULL COMMENT '语言',
  `writers` longtext NOT NULL COMMENT '作者',
  `actor` longtext NOT NULL COMMENT '演员',
  `summary` longtext NOT NULL COMMENT '简介',
  `directors` longtext NOT NULL COMMENT '导演',
  `record_time` datetime NOT NULL COMMENT '记录时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `movie_id` (`movie_id`),
  KEY `movie_collectmoviedb_year_index` (`year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `api_districts`;
CREATE TABLE `api_districts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent` int(11) NOT NULL COMMENT '父区域代号',
  `code` int(11) NOT NULL COMMENT '子区域代号',
  `name` varchar(100) NOT NULL COMMENT '区域名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `api_indexfocus`;
CREATE TABLE `api_indexfocus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `show_id` int(11) NOT NULL COMMENT '显示顺序',
  `movie_img` varchar(100) NOT NULL COMMENT '电影海报图片地址',
  `movie_content` varchar(100) NOT NULL COMMENT '描述',
  `status` int(11) NOT NULL COMMENT '显示状态',
  `movie_id_id` int(11) NOT NULL COMMENT '电影外键',
  `create_time` datetime NOT NULL COMMENT '添加时间',
  PRIMARY KEY (`id`),
  KEY `api_indexfocus_movie_id_id_d8fe64d8_fk_movie_col` (`movie_id_id`),
  CONSTRAINT `api_indexfocus_movie_id_id_d8fe64d8_fk_movie_col` FOREIGN KEY (`movie_id_id`) REFERENCES `movie_collectmoviedb` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `movie_collectmovietypedb`;
CREATE TABLE `movie_collectmovietypedb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_type` varchar(100) NOT NULL COMMENT '电影类型',
  PRIMARY KEY (`id`),
  UNIQUE KEY `movie_type` (`movie_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `movie_collecttop250moviedb`;
CREATE TABLE `movie_collecttop250moviedb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) NOT NULL COMMENT '电影ID',
  `movie_title` longtext NOT NULL COMMENT '中文标题',
  `movie_original_title` longtext NOT NULL COMMENT '原始标题',
  `movie_rating` longtext NOT NULL COMMENT '评分',
  `movie_year` int(11) NOT NULL COMMENT '年份',
  `movie_pubdates` longtext NOT NULL COMMENT '上映日期',
  `movie_directors` longtext NOT NULL COMMENT '导演',
  `movie_genres` longtext NOT NULL COMMENT '类型',
  `movie_actor` longtext NOT NULL COMMENT '演员',
  `movie_durations` longtext NOT NULL COMMENT '时长',
  `movie_collect_count` int(11) NOT NULL COMMENT '收藏数',
  `movie_mainland_pubdate` longtext NOT NULL COMMENT '主要上映日期',
  `movie_images` longtext NOT NULL COMMENT '封面图片',
  `record_time` datetime NOT NULL COMMENT '录入时间',
  PRIMARY KEY (`id`,`movie_id`) USING BTREE,
  UNIQUE KEY `movie_id` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `movie_moviepubdatedb`;
CREATE TABLE `movie_moviepubdatedb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pubdate` date DEFAULT NULL COMMENT '上映日期',
  `movie_id_id` int(11) NOT NULL COMMENT '电影',
  PRIMARY KEY (`id`),
  UNIQUE KEY `movie_id_id` (`movie_id_id`),
  CONSTRAINT `movie_moviepubdatedb_movie_id_id_bc56d562_fk_movie_col` FOREIGN KEY (`movie_id_id`) REFERENCES `movie_collectmoviedb` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `movie_movieratingdb`;
CREATE TABLE `movie_movieratingdb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rating` decimal(4,2) NOT NULL COMMENT '评分分数',
  `movie_id_id` int(11) NOT NULL COMMENT '电影',
  PRIMARY KEY (`id`),
  UNIQUE KEY `movie_movieratingdb_movie_id_id_9ccbeec7_uniq` (`movie_id_id`),
  CONSTRAINT `movie_movieratingdb_movie_id_id_9ccbeec7_fk_movie_col` FOREIGN KEY (`movie_id_id`) REFERENCES `movie_collectmoviedb` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `movie_movietagdb`;
CREATE TABLE `movie_movietagdb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_type` varchar(100) NOT NULL COMMENT '标签类型',
  `tag_name` varchar(100) NOT NULL COMMENT '标签名',
  `movie_id_id` int(11) NOT NULL COMMENT '电影',
  PRIMARY KEY (`id`),
  KEY `movie_movietagdb_movie_id_id_1b892164_fk_movie_col` (`movie_id_id`),
  KEY `movie_movietagdb_tag_name_0c47a751` (`tag_name`),
  KEY `movie_movietagdb_tag_type_dc2aa4c2` (`tag_type`),
  CONSTRAINT `movie_movietagdb_movie_id_id_1b892164_fk_movie_col` FOREIGN KEY (`movie_id_id`) REFERENCES `movie_collectmoviedb` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 2021-05-27 01:29:59
