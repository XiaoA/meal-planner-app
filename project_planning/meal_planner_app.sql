DROP DATABASE IF EXISTS meal_planner_app;

CREATE DATABASE meal_planner_app;

\c meal_planner_app

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(30) UNIQUE NOT NULL,
  password_hashed VARCHAR(264) NOT NULL,
  password_confirmation_hashed VARCHAR(264) NOT NULL
 );
 
CREATE TABLE user_profiles (
  id SERIAL PRIMARY KEY,
  username VARCHAR(15) UNIQUE NOT NULL,
  first_name VARCHAR(15),
  last_name VARCHAR(15),
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE followers (
  id SERIAL PRIMARY KEY,
  follower INTEGER REFERENCES users(id) ON DELETE CASCADE,
  followed_user INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE recipes (
  id SERIAL PRIMARY KEY,
  title VARCHAR(50) NOT NULL,
  url VARCHAR(60) NOT NULL  
);

CREATE TABLE  recipe_boxes (
  id SERIAL PRIMARY KEY,
  is_liked BOOLEAN,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE TABLE meals (
  id SERIAL PRIMARY KEY,
  meal_date DATE NOT NULL DEFAULT CURRENT_DATE,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE
);

INSERT INTO users
(id, email, password_hashed, password_confirmation_hashed)
  VALUES
  (1, 'sherlock@example.com', '$2b$14$dPp4ixbBXumqb;zW-C2*m*9J]SV@.A3U-xk', '$2b$14$dPp4ixbBXumqb;zW-C2*m*9J]SV@.A3U-xk'),
  (2, 'batman@example.com', '$2b$14YDTrPn/=jD4%.;K%qSD4[$C&TA%U4*enQ3L', '$2b$14YDTrPn/=jD4%.;K%qSD4[$C&TA%U4*enQ3L');

INSERT INTO user_profiles
(id, username, first_name, last_name, user_id)
  VALUES
  (1, 'sherlock99', 'Sherlock', 'Holmes', 1),
  (2, 'batman4u', 'Bruce', 'Wayne', 2);

INSERT INTO followers
(id, follower, followed_user)
  VALUES
  (1, 1, 2),
  (2, 2, 1);

INSERT INTO recipes
(id, title, url)
  VALUES
  (1, 'fish tacos', 'https://www.example.com/22'),
  (2, 'popcorn shrimp cakes', 'https://www.example.com/23');

INSERT INTO recipe_boxes
(id, is_liked, user_id, recipe_id)
  VALUES
  (1, TRUE, 1, 1),
  (2, FALSE, 2, 2);
  
INSERT INTO meals
(id, meal_date, user_id, recipe_id)
  VALUES
  (1, '2021-03-01', 1, 1),
  (2, '2021-04-13', 2, 2);
