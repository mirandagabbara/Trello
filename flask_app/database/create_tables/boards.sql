CREATE TABLE IF NOT EXISTS `boards` (
`board_id`           int(11)  	  NOT NULL auto_increment	        COMMENT 'id of this board',
`name`               varchar(100) NOT NULL                          COMMENT 'name of the board',
`owner_id`           int(10)  NOT NULL                 		        COMMENT 'id of the owner',
PRIMARY KEY (`board_id`),
FOREIGN KEY (owner_id) REFERENCES users(user_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains board information";