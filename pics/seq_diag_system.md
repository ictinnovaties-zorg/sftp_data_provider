```mermaid
sequenceDiagram
    User->>get_sftp_data: Request a dataset
    get_sftp_data->>SFTP server: pass credentials
    alt valid credentials
        SFTP server-->>User: data (Pandas DataFrame)
    else invalid credentials
        SFTP server-->>User: exception
    end
```