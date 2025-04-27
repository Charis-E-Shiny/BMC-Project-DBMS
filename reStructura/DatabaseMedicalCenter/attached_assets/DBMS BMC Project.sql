-- create database BMCbase;
use BMCbase;

-- Create Users Table

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'business_owner', 'investor') NOT NULL
);

-- Create Business Models Table
CREATE TABLE BusinessModels (
    model_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    business_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Customer Segments Table
CREATE TABLE CustomerSegments (
    segment_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    segment_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Customer Relationships Table
CREATE TABLE CustomerRelationships (
    relationship_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    relationship_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Value Propositions Table
CREATE TABLE ValuePropositions (
    vp_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    vp_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Channels Table
CREATE TABLE Channels (
    channel_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    channel_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Revenue Streams Table
CREATE TABLE RevenueStreams (
    revenue_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    revenue_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2),
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Cost Structure Table
CREATE TABLE CostStructure (
    cost_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    cost_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2),
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Key Resources Table
CREATE TABLE KeyResources (
    resource_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    resource_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Key Activities Table
CREATE TABLE KeyActivities (
    activity_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    activity_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Key Partnerships Table
CREATE TABLE KeyPartnerships (
    partner_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    partner_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

select * from users;


