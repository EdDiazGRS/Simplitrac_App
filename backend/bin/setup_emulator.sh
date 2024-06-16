#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to compare Java versions
compare_versions() {
    printf '%s\n%s\n' "$1" "$2" | sort -V -C
}

# Determine the standard Downloads folder
DOWNLOADS_FOLDER="$HOME/Downloads"

# Cross-platform detection for Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows-specific commands
    echo "Running on Windows..."

    # Function to check if a command exists (Windows)
    command_exists_win() {
        command -v "$1" >/dev/null 2>&1 || where "$1" >/dev/null 2>&1
    }

    # Check if git is installed
    if ! command_exists_win git; then
        echo "Git is not installed. Please install it first."
        exit 1
    fi

    # Pull the latest code from GitHub
    echo "Pulling the latest code from GitHub..."
    git pull

    echo "Script completed successfully."

    # Check Java version
    JAVA_VERSION=$(java -version 2>&1 | findstr /i "version" | awk -F '"' '{print $2}')
    REQUIRED_VERSION="17.0.11"

    # Download and install Java if not installed or version is less than 17
    if ! command_exists_win java || ! compare_versions "$JAVA_VERSION" "$REQUIRED_VERSION"; then
        echo "Java 17 is not installed. Installing Java 17..."

        # Define the download URL for Windows
        JAVA_DOWNLOAD_URL="https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.zip"
        JAVA_ZIP_FILE="$DOWNLOADS_FOLDER/jdk-17.zip"

        # Download the Java installer using curl or PowerShell
        if command_exists_win curl; then
            echo "Downloading Java 17 using curl to $JAVA_ZIP_FILE..."
            curl -L -o "$JAVA_ZIP_FILE" "$JAVA_DOWNLOAD_URL"
        else
            echo "curl is not installed. Using PowerShell to download..."
            powershell -Command "Invoke-WebRequest -Uri '$JAVA_DOWNLOAD_URL' -OutFile '$JAVA_ZIP_FILE'"
        fi

        # Extract and install Java
        echo "Extracting Java 17 to %PROGRAMFILES%..."
        powershell -Command "Expand-Archive -Path '$JAVA_ZIP_FILE' -DestinationPath '$PROGRAMFILES%/Java' -Force"

        # Set up Java path for Windows
        JAVA_HOME="$PROGRAMFILES/Java/jdk-17"

        # Update JAVA_HOME and PATH for the current session
        setx JAVA_HOME "$JAVA_HOME"
        setx PATH "$JAVA_HOME/bin;$PATH"

        echo "Java 17 installed successfully and JAVA_HOME set to $JAVA_HOME."
    else
        echo "Java 17 is already installed."
    fi

    # Check if Firebase CLI is installed
    if ! command_exists_win firebase; then
        echo "Firebase CLI is not installed. Please install it first."
        exit 1
    fi

    echo "You should now be ready to start the virtual environment"
    echo "Run: 'firebase emulators:start' to start the emulators"

else
    # macOS or Linux-specific commands
    echo "Running on macOS or Linux..."

    # Check if git is installed
    if ! command_exists git; then
        echo "Git is not installed. Please install it first."
        exit 1
    fi

    # Pull the latest code from GitHub
    echo "Pulling the latest code from GitHub..."
    git pull

    echo "Script completed successfully."

    # Check Java version
    JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    REQUIRED_VERSION="17.0.11"

    # Download and install Java if not installed or version is less than 17
    if ! command_exists java || ! compare_versions "$JAVA_VERSION" "$REQUIRED_VERSION"; then
        echo "Java 17 is not installed. Installing Java 17..."

        # Define the download URL based on the OS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            JAVA_DOWNLOAD_URL="https://download.oracle.com/java/17/latest/jdk-17_macos-x64_bin.tar.gz"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            JAVA_DOWNLOAD_URL="https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz"
        else
            echo "Unsupported OS type: $OSTYPE"
            exit 1
        fi

        # Define the target file path in the Downloads folder
        JAVA_TAR_FILE="$DOWNLOADS_FOLDER/jdk-17.tar.gz"

        # Download the Java installer using curl
        if command_exists curl; then
            echo "Downloading Java 17 using curl to $JAVA_TAR_FILE..."
            curl -L -o "$JAVA_TAR_FILE" "$JAVA_DOWNLOAD_URL"
        else
            echo "curl is not installed. Please install curl or wget."
            exit 1
        fi

        # Extract and install Java
        sudo mkdir -p /usr/local/java
        sudo tar -xvf "$JAVA_TAR_FILE" -C /usr/local/java

        # Set up Java path based on OS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            JAVA_HOME="/usr/local/java/jdk-17.jdk/Contents/Home"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            JAVA_HOME="/usr/local/java/jdk-17"
        fi

        # Update JAVA_HOME and PATH for the current session
        export JAVA_HOME="$JAVA_HOME"
        export PATH="$JAVA_HOME/bin:$PATH"

        # Add Java to system profile for future sessions
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 17)' >> ~/.zshrc
            echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.zshrc
            source ~/.zshrc
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "export JAVA_HOME=\"$JAVA_HOME\"" >> ~/.bashrc
            echo "export PATH=\"$JAVA_HOME/bin:\$PATH\"" >> ~/.bashrc
            source ~/.bashrc
        fi

        echo "Java 17 installed successfully and JAVA_HOME set to $JAVA_HOME."
    else
        echo "Java 17 is already installed."
    fi

    # Check if Firebase CLI is installed
    if ! command_exists firebase; then
        echo "Firebase CLI is not installed. Please install it first."
        exit 1
    fi

    # Refresh your .zshrc or .bashrc file
    if [[ -f ~/.zshrc ]]; then
        source ~/.zshrc
    elif [[ -f ~/.bashrc ]]; then
        source ~/.bashrc
    fi

    echo "You should now be ready to start the virtual environment"
    echo "Run: 'firebase emulators:start' to start the emulators"
fi
