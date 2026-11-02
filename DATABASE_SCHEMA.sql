-- MySQL schema-only export generated from app/model SQLAlchemy metadata.

-- Alembic migrations are the source of truth for changes.

-- Select the intended database before running this file.

CREATE TABLE campuses (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	code VARCHAR(30) NOT NULL, 
	name VARCHAR(150) NOT NULL, 
	address TEXT, 
	PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_campuses_code ON campuses (code);

CREATE TABLE categories (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	parent_category_id INTEGER, 
	name VARCHAR(100) NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_category_id) REFERENCES categories (id) ON DELETE SET NULL
);

CREATE UNIQUE INDEX ix_categories_name ON categories (name);

CREATE INDEX ix_categories_parent_category_id ON categories (parent_category_id);

CREATE TABLE permissions (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	code VARCHAR(100) NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_permissions_code ON permissions (code);

CREATE TABLE roles (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(50) NOT NULL, 
	description TEXT, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_roles_name ON roles (name);

CREATE TABLE users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username VARCHAR(50) NOT NULL, 
	email VARCHAR(254) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	first_name VARCHAR(100), 
	last_name VARCHAR(100), 
	is_active BOOL NOT NULL DEFAULT 1, 
	email_verified_at DATETIME, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE UNIQUE INDEX ix_users_username ON users (username);

CREATE TABLE audit_logs (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	actor_user_id INTEGER, 
	action VARCHAR(50) NOT NULL, 
	entity_type VARCHAR(100) NOT NULL, 
	entity_id INTEGER, 
	before_data JSON, 
	after_data JSON, 
	ip_address VARCHAR(45), 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(actor_user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE INDEX ix_audit_logs_actor_user_id ON audit_logs (actor_user_id);

CREATE TABLE locations (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	campus_id INTEGER NOT NULL, 
	parent_location_id INTEGER, 
	name VARCHAR(150) NOT NULL, 
	location_type VARCHAR(30) NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_location_sibling_name UNIQUE (campus_id, parent_location_id, name), 
	FOREIGN KEY(campus_id) REFERENCES campuses (id) ON DELETE RESTRICT, 
	FOREIGN KEY(parent_location_id) REFERENCES locations (id) ON DELETE SET NULL
);

CREATE TABLE role_permission (
	role_id INTEGER NOT NULL, 
	permission_id INTEGER NOT NULL, 
	granted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (role_id, permission_id), 
	FOREIGN KEY(role_id) REFERENCES roles (id) ON DELETE CASCADE, 
	FOREIGN KEY(permission_id) REFERENCES permissions (id) ON DELETE CASCADE
);

CREATE TABLE user_role (
	user_id INTEGER NOT NULL, 
	role_id INTEGER NOT NULL, 
	granted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	granted_by_user_id INTEGER, 
	PRIMARY KEY (user_id, role_id), 
	CONSTRAINT fk_user_role_user FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	CONSTRAINT fk_user_role_role FOREIGN KEY(role_id) REFERENCES roles (id) ON DELETE CASCADE, 
	CONSTRAINT fk_user_role_granted_by FOREIGN KEY(granted_by_user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE item_reports (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	report_type VARCHAR(10) NOT NULL, 
	status VARCHAR(20) NOT NULL DEFAULT 'OPEN', 
	reporter_user_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	location_id INTEGER, 
	title VARCHAR(150) NOT NULL, 
	description TEXT NOT NULL, 
	brand VARCHAR(100), 
	color VARCHAR(60), 
	distinctive_features TEXT, 
	occurred_at DATETIME, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_item_reports_report_type CHECK (report_type IN ('LOST', 'FOUND')), 
	CONSTRAINT ck_item_reports_status CHECK (status IN ('OPEN', 'UNDER_REVIEW', 'RESOLVED', 'CLOSED', 'WITHDRAWN')), 
	FOREIGN KEY(reporter_user_id) REFERENCES users (id) ON DELETE RESTRICT, 
	FOREIGN KEY(category_id) REFERENCES categories (id) ON DELETE RESTRICT, 
	FOREIGN KEY(location_id) REFERENCES locations (id) ON DELETE SET NULL
);

CREATE INDEX ix_item_reports_category_id ON item_reports (category_id);

CREATE INDEX ix_item_reports_location_id ON item_reports (location_id);

CREATE INDEX ix_item_reports_reporter_user_id ON item_reports (reporter_user_id);

CREATE INDEX ix_item_reports_type_status ON item_reports (report_type, status);

CREATE TABLE item_claims (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	report_id INTEGER NOT NULL, 
	claimant_user_id INTEGER NOT NULL, 
	status VARCHAR(20) NOT NULL DEFAULT 'SUBMITTED', 
	claim_details TEXT NOT NULL, 
	review_note TEXT, 
	reviewed_by_user_id INTEGER, 
	reviewed_at DATETIME, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_item_claim_report_claimant UNIQUE (report_id, claimant_user_id), 
	CONSTRAINT ck_item_claims_status CHECK (status IN ('SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'REJECTED', 'WITHDRAWN')), 
	FOREIGN KEY(report_id) REFERENCES item_reports (id) ON DELETE RESTRICT, 
	FOREIGN KEY(claimant_user_id) REFERENCES users (id) ON DELETE RESTRICT, 
	FOREIGN KEY(reviewed_by_user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE INDEX ix_item_claims_claimant_user_id ON item_claims (claimant_user_id);

CREATE INDEX ix_item_claims_report_id ON item_claims (report_id);

CREATE TABLE item_report_photos (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	report_id INTEGER NOT NULL, 
	storage_key VARCHAR(500) NOT NULL, 
	uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(report_id) REFERENCES item_reports (id) ON DELETE CASCADE, 
	UNIQUE (storage_key)
);

CREATE INDEX ix_item_report_photos_report_id ON item_report_photos (report_id);

CREATE TABLE notifications (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	recipient_user_id INTEGER NOT NULL, 
	report_id INTEGER, 
	notification_type VARCHAR(50) NOT NULL, 
	message TEXT NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	read_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipient_user_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(report_id) REFERENCES item_reports (id) ON DELETE SET NULL
);

CREATE INDEX ix_notifications_recipient_user_id ON notifications (recipient_user_id);

CREATE INDEX ix_notifications_report_id ON notifications (report_id);

CREATE TABLE report_matches (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	lost_report_id INTEGER NOT NULL, 
	found_report_id INTEGER NOT NULL, 
	created_by_user_id INTEGER, 
	status VARCHAR(20) NOT NULL DEFAULT 'PROPOSED', 
	confidence_score NUMERIC(5, 2), 
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_report_match_pair UNIQUE (lost_report_id, found_report_id), 
	CONSTRAINT ck_report_matches_distinct_reports CHECK (lost_report_id <> found_report_id), 
	CONSTRAINT ck_report_matches_status CHECK (status IN ('PROPOSED', 'CONFIRMED', 'DISMISSED')), 
	CONSTRAINT ck_report_matches_confidence CHECK (confidence_score IS NULL OR confidence_score BETWEEN 0 AND 100), 
	FOREIGN KEY(lost_report_id) REFERENCES item_reports (id) ON DELETE RESTRICT, 
	FOREIGN KEY(found_report_id) REFERENCES item_reports (id) ON DELETE RESTRICT, 
	FOREIGN KEY(created_by_user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE INDEX ix_report_matches_found_report_id ON report_matches (found_report_id);

CREATE INDEX ix_report_matches_lost_report_id ON report_matches (lost_report_id);
