CREATE DATABASE emoprobe;

USE emoprobe;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `comment_id` int NOT NULL AUTO_INCREMENT COMMENT '评论编号',
  `user_uid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论者uid',
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论者用户名',
  `user_ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '评论者ip地址',
  `user_sex` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论者性别',
  `comment_date` datetime NOT NULL COMMENT '评论时间',
  `comment_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论内容',
  `comment_like` int NOT NULL COMMENT '点赞数',
  `comment_reply` int NOT NULL COMMENT '回复数',
  `comment_emotion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '情绪鉴定',
  `video_bvid` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '归属视频',
  PRIMARY KEY (`comment_id`),
  KEY `video_bvid` (`video_bvid`),
  CONSTRAINT `video_bvid` FOREIGN KEY (`video_bvid`) REFERENCES `video` (`video_bvid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26801 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Table structure for sentence
-- ----------------------------
DROP TABLE IF EXISTS `sentence`;
CREATE TABLE `sentence` (
  `sentence_id` int NOT NULL AUTO_INCREMENT,
  `sentence_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `sentence_emotion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `sentence_savetime` datetime DEFAULT NULL,
  PRIMARY KEY (`sentence_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1309 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for video
-- ----------------------------
DROP TABLE IF EXISTS `video`;
CREATE TABLE `video` (
  `video_bvid` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '视频bv号',
  `video_aid` varchar(20) NOT NULL COMMENT '视频av号',
  `owner_uid` varchar(20) NOT NULL COMMENT '发布者uid',
  `owner_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '发布者用户名',
  `video_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '视频名',
  `video_partition` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '视频分区',
  `video_tables` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '视频标签',
  `video_pubdate` datetime NOT NULL COMMENT '视频发布时间',
  `video_duration` int NOT NULL COMMENT '视频时长（秒）',
  `video_like` int NOT NULL COMMENT '点赞数',
  `video_coin` int NOT NULL COMMENT '投币数',
  `video_favorite` int NOT NULL COMMENT '收藏数',
  `video_share` int NOT NULL COMMENT '分享数',
  `video_reply` int NOT NULL,
  `video_dislike` int NOT NULL COMMENT '点踩数',
  `video_cid` varchar(20) NOT NULL COMMENT '用于爬虫',
  `video_savedate` datetime NOT NULL COMMENT '处理该视频的日期',
  `video_desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '视频简介',
  PRIMARY KEY (`video_bvid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
