

DROP TABLE IF EXISTS `business`;

CREATE TABLE `business` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) DEFAULT NULL,
  `telefone` varchar(9) DEFAULT NULL,
  `morada` varchar(100) DEFAULT NULL,
  `cod` varchar(12) DEFAULT NULL,
  `freguesia` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump da tabela users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(30) DEFAULT '',
  `email` varchar(50) DEFAULT '',
  `password` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `constraint_name` (`username`,`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
