CREATE TABLE `homework_info` (
  `rec_id` int NOT NULL AUTO_INCREMENT,
  `c_name` varchar(32) DEFAULT NULL,
  `assigntime` date DEFAULT NULL,
  `detail` varchar(1024) DEFAULT NULL,
  `deadline` datetime DEFAULT NULL,
  `method` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`rec_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci