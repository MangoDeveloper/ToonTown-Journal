CREATE TABLE `Accounts` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL DEFAULT '0',
  `password` varchar(255) NOT NULL DEFAULT '0',
  `rawPassword` tinyint(4) NOT NULL DEFAULT '0',
  `email` varchar(255) NOT NULL DEFAULT '0',
  `accountid` int(11) NOT NULL DEFAULT '0',
  `adminAccess` int(11) NOT NULL DEFAULT '0',
  `canPlay` int(10) DEFAULT '1',
  `ipBanned` int(10) DEFAULT '0',
  `banReason` varchar(255) NOT NULL DEFAULT '0',
  `banRelease` varchar(30) NOT NULL DEFAULT '0',
  `bannedTime` varchar(30) NOT NULL DEFAULT '0',
  `banBy` varchar(20) NOT NULL DEFAULT '0',
  `status` text,
  `name` varchar(25) NOT NULL DEFAULT '0',
  `newsname` varchar(25) NOT NULL DEFAULT '0',
  `allowemails` tinyint(10) NOT NULL DEFAULT '1',
  `rpwkey` varchar(100) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Actions` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `currentTime` varchar(20) NOT NULL,
  `releaseTime` varchar(20) NOT NULL,
  `type` varchar(100) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `actedBy` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `ChatAudit` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `time` int(11) NOT NULL,
  `sender` varchar(40) NOT NULL,
  `message` varchar(255) NOT NULL,
  `channel` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Messages` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `time` int(11) NOT NULL,
  `category` varchar(40) NOT NULL,
  `description` varchar(40) NOT NULL,
  `sender` varchar(10) NOT NULL,
  `receiver` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `NameApprovals` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `avid` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `status` varchar(10) NOT NULL,
  `reviewedby` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Toons` (
  `id`          int(10) NOT NULL AUTO_INCREMENT,
  `accountid`   int(11) NOT NULL,
  `toonid`      int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `toonid` (`toonid`)
) ENGINE=InnoDB;
