# Snowflake Flyway Pipeline

This project provides a GitHub Actions pipeline for executing Flyway migrations against a Snowflake database. It automates the process of applying database schema changes using SQL migration scripts.

## Project Structure

```
snowflake-flyway-pipeline
├── .github
│   └── workflows
│       └── flyway.yml        # GitHub Actions workflow for Flyway migrations
├── scripts
│   └── migrate.sql           # SQL migration scripts for Snowflake
├── flyway.conf               # Configuration file for Flyway
├── package.json              # npm configuration file
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd snowflake-flyway-pipeline
   ```

2. **Install Dependencies**
   Ensure you have Node.js installed, then run:
   ```bash
   npm install
   ```

3. **Configure Flyway**
   Update the `flyway.conf` file with your Snowflake database connection details, including user credentials and migration script locations.

4. **Create Migration Scripts**
   Add your SQL migration scripts in the `scripts/migrate.sql` file. Ensure that the scripts are written in accordance with Flyway's migration naming conventions.

## Usage Guidelines

- The GitHub Actions workflow defined in `.github/workflows/flyway.yml` will automatically trigger on specified events (e.g., push, pull request) to execute the migrations.
- Monitor the Actions tab in your GitHub repository to view the status of the migration runs.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

# How it works:

When you manually trigger the workflow, you choose the environment.
For preprod and prod, you can set up environment protection rules in your repo settings for manual approval.

# To set up approvals:

Go to your repo → Settings → Environments → Add preprod and prod environments.
Add required reviewers for those environments.
Now, the workflow will run immediately for dev, but require approval for preprod and prod.