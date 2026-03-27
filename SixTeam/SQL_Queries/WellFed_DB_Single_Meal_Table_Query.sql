USE `WellFed_DB`;

CREATE TABLE meal_planner_single_meal (
	meal_id INT AUTO_INCREMENT,
    user_id INT, 
    meal_name VARCHAR(300),
    recipe_link VARCHAR(500),
    recipe_image_filename VARCHAR(300),
    meal_type VARCHAR(150),
    PRIMARY KEY (meal_id, user_id)
);
