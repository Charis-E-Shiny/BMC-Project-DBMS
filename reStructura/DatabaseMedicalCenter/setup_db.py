#!/usr/bin/env python
# Script to set up the database schema

import os
import sys
from db_config import get_db_connection

# MySQL Schema Creation SQL
MYSQL_SCHEMA = """
-- Create Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'business_owner', 'investor') NOT NULL
);

-- Create Business Models Table
CREATE TABLE IF NOT EXISTS BusinessModels (
    model_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    business_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Customer Segments Table
CREATE TABLE IF NOT EXISTS CustomerSegments (
    segment_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    segment_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Customer Relationships Table
CREATE TABLE IF NOT EXISTS CustomerRelationships (
    relationship_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    relationship_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Value Propositions Table
CREATE TABLE IF NOT EXISTS ValuePropositions (
    vp_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    vp_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Channels Table
CREATE TABLE IF NOT EXISTS Channels (
    channel_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    channel_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Revenue Streams Table
CREATE TABLE IF NOT EXISTS RevenueStreams (
    revenue_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    revenue_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2),
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Cost Structure Table
CREATE TABLE IF NOT EXISTS CostStructure (
    cost_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    cost_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2),
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Key Resources Table
CREATE TABLE IF NOT EXISTS KeyResources (
    resource_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    resource_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Key Activities Table
CREATE TABLE IF NOT EXISTS KeyActivities (
    activity_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    activity_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Key Partnerships Table
CREATE TABLE IF NOT EXISTS KeyPartnerships (
    partner_id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT,
    partner_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);
"""

# PostgreSQL Schema Creation SQL
POSTGRES_SCHEMA = """
-- Create Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'business_owner', 'investor'))
);

-- Create Business Models Table
CREATE TABLE IF NOT EXISTS BusinessModels (
    model_id SERIAL PRIMARY KEY,
    user_id INT,
    business_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Customer Segments Table
CREATE TABLE IF NOT EXISTS CustomerSegments (
    segment_id SERIAL PRIMARY KEY,
    model_id INT,
    segment_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Customer Relationships Table
CREATE TABLE IF NOT EXISTS CustomerRelationships (
    relationship_id SERIAL PRIMARY KEY,
    model_id INT,
    relationship_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Value Propositions Table
CREATE TABLE IF NOT EXISTS ValuePropositions (
    vp_id SERIAL PRIMARY KEY,
    model_id INT,
    vp_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Channels Table
CREATE TABLE IF NOT EXISTS Channels (
    channel_id SERIAL PRIMARY KEY,
    model_id INT,
    channel_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Revenue Streams Table
CREATE TABLE IF NOT EXISTS RevenueStreams (
    revenue_id SERIAL PRIMARY KEY,
    model_id INT,
    revenue_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2),
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Cost Structure Table
CREATE TABLE IF NOT EXISTS CostStructure (
    cost_id SERIAL PRIMARY KEY,
    model_id INT,
    cost_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2),
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Key Resources Table
CREATE TABLE IF NOT EXISTS KeyResources (
    resource_id SERIAL PRIMARY KEY,
    model_id INT,
    resource_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Key Activities Table
CREATE TABLE IF NOT EXISTS KeyActivities (
    activity_id SERIAL PRIMARY KEY,
    model_id INT,
    activity_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);

-- Create Key Partnerships Table
CREATE TABLE IF NOT EXISTS KeyPartnerships (
    partner_id SERIAL PRIMARY KEY,
    model_id INT,
    partner_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (model_id) REFERENCES BusinessModels(model_id) ON DELETE CASCADE
);
"""

def main():
    print("Setting up the database schema...")
    conn = None
    try:
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Determine database type (MySQL or PostgreSQL)
        db_type = "postgres" if os.environ.get('DATABASE_URL') else "mysql"
        
        # Execute appropriate schema SQL
        if db_type == "mysql":
            print("Using MySQL schema")
            for statement in MYSQL_SCHEMA.split(';'):
                if statement.strip():
                    cursor.execute(statement)
        else:
            print("Using PostgreSQL schema")
            for statement in POSTGRES_SCHEMA.split(';'):
                if statement.strip():
                    cursor.execute(statement)
        
        conn.commit()
        print("Database schema created successfully!")
    except Exception as e:
        print(f"Error setting up database: {e}", file=sys.stderr)
        return 1
    finally:
        if conn:
            conn.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())