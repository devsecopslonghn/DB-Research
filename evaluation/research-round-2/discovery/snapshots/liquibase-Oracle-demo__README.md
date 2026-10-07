# Oracle Database Demo with Azure DevOps

## Overview
This repository demonstrates Oracle database schema management using Liquibase with Azure DevOps CI/CD integration. It showcases environment-specific deployments, structured changelog organization, and enterprise-grade deployment workflows suitable for Oracle-based applications.

## Implementation Summary

### Core Implementation Patterns

This repository demonstrates Oracle database schema management using Liquibase with Azure DevOps integration. Key patterns include:

- **Environment-specific schema naming**: Uses dynamic properties to target different schemas (CMS_DEV, CMS_QA, CMS) based on deployment context
- **Structured changelog organization**: Separates DDL, stored procedures, and DML into logical directories (100_ddl, 200_procedures, 700_dml)
- **Azure Pipeline integration**: Implements Liquibase Flow execution within Azure DevOps using PowerShell tasks
- **Multi-environment deployment**: Supports DEV, QA, and PROD environments with different connection parameters

### Reusable Components

- **Environment property configuration**: The property-based schema naming pattern can be extracted for any multi-environment Oracle setup
- **Azure Pipeline template**: The pipeline YAML structure provides a reusable template for Liquibase Flow execution
- **Directory structure**: The numbered directory approach (100_ddl, 200_procedures, etc.) provides clear organization for complex Oracle schemas
- **Liquibase Flow configuration**: The flow file demonstrates advanced deployment workflows

### Customer Adaptation Points

- **Database connection**: Update `liquibase.properties` with customer-specific Oracle connection details
- **Schema naming**: Modify the property definitions in `changelog.xml` to match customer schema naming conventions
- **Pipeline variables**: Adjust Azure Pipeline variables (URL, USERNAME, PASSWORD, PRO_LICENSE_KEY) for customer environments
- **Directory organization**: Adapt the numbered directory structure to match customer's database organization preferences
- **Environment contexts**: Add or modify environment contexts (DEV/QA/PROD) to match customer deployment stages

### Common Customizations

- **Additional environments**: Add staging, UAT, or other environment contexts
- **Oracle-specific features**: Leverage Oracle tablespaces, partitioning, or advanced security features
- **Approval workflows**: Integrate Azure DevOps approval gates for production deployments
- **Rollback strategies**: Implement automated rollback procedures for failed deployments
- **Monitoring integration**: Add health checks and deployment notifications

### Troubleshooting Patterns

- **Connection issues**: Verify Oracle TNS configuration and network connectivity
- **Schema permissions**: Ensure the Liquibase user has appropriate DDL/DML permissions on target schemas
- **Environment variable problems**: Check Azure Pipeline variable configuration and scoping
- **Liquibase Flow errors**: Validate the flow file syntax and ensure Pro license is active
- **Changelog execution failures**: Use `liquibase status` to verify changelog state before deployments

## Use Case
Enterprise Oracle database schema evolution with automated CI/CD deployment across multiple environments. Ideal for customers managing complex Oracle schemas requiring structured change management and approval workflows.

## What You'll Learn
- Oracle-specific Liquibase configuration patterns
- Azure DevOps pipeline integration with Liquibase
- Multi-environment schema deployment strategies
- Liquibase Flow for advanced deployment workflows
- Enterprise-grade Oracle change management

## Prerequisites
- Oracle Database 11g or higher
- Liquibase Pro license
- Azure DevOps with Windows build agents
- Oracle JDBC driver
- PowerShell execution capabilities

## Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/liquibase-examples/liquibase-Oracle-demo.git
cd liquibase-Oracle-demo
```

### 2. Database Setup
```bash
# Ensure Oracle database is running and accessible
# Create the target schemas (CMS_DEV, CMS_QA, CMS)
# Grant appropriate permissions to liquibase_user
```

### 3. Configure Liquibase
```bash
# Update liquibase.properties with your Oracle connection details
# Set the appropriate URL, username, and password
# Ensure Liquibase Pro license key is available
```

### 4. Run Initial Migration
```bash
# For local testing (replace with your context)
liquibase --contexts=DEV update
```

## Repository Structure
```
├── main/
│   ├── 100_ddl/           # Data Definition Language changes
│   ├── 200_procedures/    # Stored procedures
│   └── 700_dml/          # Data Manipulation Language changes
├── azure-pipelines.yml   # Azure DevOps pipeline configuration
├── changelog.xml         # Main Liquibase changelog
├── liquibase.properties  # Database connection properties
├── liquibase.flowfile.yaml  # Liquibase Flow configuration
└── commands.sh          # Utility scripts
```

## Key Features Demonstrated

### Environment-Specific Schema Targeting
The repository uses Liquibase properties to dynamically target different schemas based on deployment context, enabling the same changelog to deploy to DEV, QA, and PROD environments.

### Azure DevOps Integration
Complete Azure Pipeline configuration showing how to execute Liquibase Flow commands within enterprise CI/CD workflows using PowerShell tasks.

### Structured Change Organization
Demonstrates best practices for organizing Oracle database changes into logical categories (DDL, procedures, DML) for maintainable schema evolution.

## Configuration

### Environment Variables (Azure Pipeline)
| Variable | Description | Required |
|----------|-------------|----------|
| `URL` | Oracle database JDBC URL | Yes |
| `USERNAME` | Database username | Yes |
| `PASSWORD` | Database password | Yes |
| `CHANGELOG` | Path to changelog file | Yes |
| `PRO_LICENSE_KEY` | Liquibase Pro license key | Yes |

### Liquibase Properties
Key configuration options in `liquibase.properties`:
- `changeLogFile`: Points to the main changelog.xml file
- `url`: Oracle JDBC connection string
- `username/password`: Database authentication credentials

## Deployment Workflows

### Development Environment
1. Developer commits changes to feature branch
2. Azure Pipeline validates changelog syntax
3. Automated deployment to DEV schema (CMS_DEV)
4. Validation tests execute

### QA Environment
1. Pull request merged to main branch
2. Pipeline deploys to QA schema (CMS_QA)
3. Automated testing suite runs
4. QA team validation

### Production Environment
1. Release branch created from main
2. Manual approval gate triggered
3. Deployment to PROD schema (CMS)
4. Post-deployment verification

## Common Operations

### Adding a New Migration
```bash
# Create new changeset in appropriate directory
# Update changelog.xml to include the new file
# Test locally before committing
```

### Rolling Back Changes
```bash
# Use Liquibase rollback commands
liquibase rollback-count 1 --contexts=DEV
```

### Checking Database Status
```bash
# Verify current database state
liquibase status --contexts=DEV
```

## Additional Resources
- [Liquibase Oracle Documentation](https://docs.liquibase.com/databases/oracle/oracle.html)
- [Azure DevOps Pipeline Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Liquibase Pro Features](https://www.liquibase.com/pro)

## Support
For issues related to this implementation pattern, please refer to the troubleshooting section above or consult the Liquibase documentation.