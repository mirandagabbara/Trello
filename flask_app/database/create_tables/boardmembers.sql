CREATE TABLE IF NOT EXISTS `boardmembers` (
`member_id`         int(11)  	   NOT NULL auto_increment	      COMMENT 'the id of the member',
`board_id`            int(10)  NOT NULL                   COMMENT 'id of the board',
`user_id`           int(10) NOT NULL            		  COMMENT 'id of the user',
PRIMARY KEY (`member_id`),
FOREIGN KEY (board_id) REFERENCES boards(board_id),
FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains board member information";