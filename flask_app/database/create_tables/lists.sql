CREATE TABLE IF NOT EXISTS `lists` (
`list_id`         int(11)  	   NOT NULL auto_increment	      COMMENT 'the id of this list',
`board_id`        int(10)  NOT NULL                     COMMENT 'id of the board',
`owner_id`        int(10)  NOT NULL              		  COMMENT 'id of the owner',
PRIMARY KEY (`list_id`),
FOREIGN KEY (board_id) REFERENCES boards(board_id),
FOREIGN KEY (owner_id) REFERENCES users(user_id)

) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains board list information";