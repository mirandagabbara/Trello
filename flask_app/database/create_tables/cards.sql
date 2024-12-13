CREATE TABLE IF NOT EXISTS `cards` (
`card_id`            int(11)  	  NOT NULL auto_increment	      COMMENT 'the id of this card',
`list_id`            int(10)  NOT NULL                              COMMENT 'id of the card',
`content`           varchar(100) NOT NULL            		        COMMENT 'id of the owner',
`is_locked`         BOOLEAN DEFAULT FALSE                          COMMENT 'is the card locked?',
PRIMARY KEY (`card_id`),
FOREIGN KEY (list_id) REFERENCES lists(list_id)

) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains card information";