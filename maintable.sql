CREATE TABLE `sm9` (
  `id` bigint DEFAULT NULL,
  `commentno` int DEFAULT NULL,
  `commentposition` bigint DEFAULT NULL,
  `commentcontent` varchar(1200) DEFAULT NULL,
  `commentcommand` varchar(200) DEFAULT NULL,
  `userid` varchar(100) DEFAULT NULL,
  `posttime` datetime DEFAULT NULL,
  `nicoru` smallint DEFAULT NULL,
  `commentcontent_kana` varchar(2400) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci