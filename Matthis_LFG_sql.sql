-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema LFG_Schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `LFG_Schema` ;

-- -----------------------------------------------------
-- Schema LFG_Schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `LFG_Schema` DEFAULT CHARACTER SET utf8 ;
USE `LFG_Schema` ;

-- -----------------------------------------------------
-- Table `LFG_Schema`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LFG_Schema`.`Users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(25) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `about_me` TEXT NULL,
  `availability` VARCHAR(45) NULL,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `updated_at` DATETIME NOT NULL DEFAULT now() on update now(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFG_Schema`.`Comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LFG_Schema`.`Comments` (
  `comment_id` INT NOT NULL AUTO_INCREMENT,
  `body` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT now(),
  `updated_at` DATETIME NOT NULL DEFAULT now() on update now(),
  `commenter_id` INT NOT NULL,
  `commenti_id` INT NOT NULL,
  INDEX `fk_Users_has_Users_Users1_idx` (`commenti_id` ASC) VISIBLE,
  INDEX `fk_Users_has_Users_Users_idx` (`commenter_id` ASC) VISIBLE,
  PRIMARY KEY (`comment_id`),
  CONSTRAINT `fk_Users_has_Users_Users`
    FOREIGN KEY (`commenter_id`)
    REFERENCES `LFG_Schema`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Users_has_Users_Users1`
    FOREIGN KEY (`commenti_id`)
    REFERENCES `LFG_Schema`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFG_Schema`.`Consoles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LFG_Schema`.`Consoles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `image` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFG_Schema`.`Games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LFG_Schema`.`Games` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `image` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFG_Schema`.`Users_has_Consoles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LFG_Schema`.`Users_has_Consoles` (
  `user_id` INT NOT NULL,
  `console_id` INT NOT NULL,
  INDEX `fk_Users_has_Consoles_Consoles1_idx` (`console_id` ASC) VISIBLE,
  INDEX `fk_Users_has_Consoles_Users1_idx` (`user_id` ASC) VISIBLE,
  PRIMARY KEY (`user_id`, `console_id`),
  CONSTRAINT `fk_Users_has_Consoles_Users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `LFG_Schema`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Users_has_Consoles_Consoles1`
    FOREIGN KEY (`console_id`)
    REFERENCES `LFG_Schema`.`Consoles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFG_Schema`.`Users_has_Games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LFG_Schema`.`Users_has_Games` (
  `user_id` INT NOT NULL,
  `game_id` INT NOT NULL,
  INDEX `fk_Users_has_Games_Games1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_Users_has_Games_Users1_idx` (`user_id` ASC) VISIBLE,
  PRIMARY KEY (`user_id`, `game_id`),
  CONSTRAINT `fk_Users_has_Games_Users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `LFG_Schema`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Users_has_Games_Games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `LFG_Schema`.`Games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
