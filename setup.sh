#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

MAC_OS="MacOS"
LINUX="Linux"

function error() {
  # shellcheck disable=SC2059
  printf "${RED}$1${NC}" && echo ""
}

function usage() {
  cat - >&2 <<EOF
NAME
    setup.sh - Setup script for ModularHistory development

SYNOPSIS
    setup.sh [-h|--help]
    setup.sh
    setup.sh [--noninteractive] [--no-installation]

OPTIONS
  -h, --help
      Prints this and exits

  --noninteractive
      Option that makes the script run without user input

  --skip-dependencies
      Option that makes the script skip installing dependencies with Poetry/Pip

  --skip-dev-dependencies
      Option that makes the script skip installing dev dependencies with Poetry/Pip

  --
      Specify end of options; useful if the first non option
      argument starts with a hyphen

EOF
}

function fatal() {
  for i; do
    echo -e "${i}" >&2
  done
  exit 1
}

# For long option processing
function next_arg() {
  if [[ $OPTARG == *=* ]]; then
    # for cases like '--opt=arg'
    OPTARG="${OPTARG#*=}"
  else
    # for cases like '--opt arg'
    OPTARG="${args[$OPTIND]}"
    OPTIND=$((OPTIND + 1))
  fi
}

# ':' means preceding option character expects one argument, except
# first ':' which make getopts run in silent mode. We handle errors with
# wildcard case catch. Long options are considered as the '-' character
optspec=":hfb:-:"
args=("" "$@") # dummy first element so $1 and $args[1] are aligned
while getopts "$optspec" optchar; do
  case "$optchar" in
  h)
    usage
    exit 0
    ;;
  -) # long option processing
    case "$OPTARG" in
    help)
      usage
      exit 0
      ;;
    noninteractive)
      noninteractive=true
      ;;
    skip-dependencies)
      skip_dependencies=true
      ;;
    skip-dev-dependencies)
      skip_dev_dependencies=true
      ;;
    -) break ;;
    *) fatal "Unknown option '--${OPTARG}'" "See '${0} --help' for usage" ;;
    esac
    ;;
  *) fatal "Unknown option: '-${OPTARG}'" "See '${0} --help' for usage" ;;
  esac
done

shift $((OPTIND - 1))

if [[ "$noninteractive" == true ]]; then
  interactive=false
else
  interactive=true
fi

# Detect operating system
os_name=$(uname -s)
if [[ "$os_name" == Darwin* ]]; then
  os='MacOS'
elif [[ "$os_name" == Linux* ]]; then
  os='Linux'
elif [[ "$os_name" == Windows* ]]; then
  os='Windows'
else
  error "Detected unknown operating system."
  exit 1
fi
echo "Detected $os."

# Update package managers
echo "Checking package manager..."
if [[ "$os" == "$MAC_OS" ]]; then
  # Install/update Homebrew
  brew help &>/dev/null || {
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
  }
  echo "Updating packages..."
  brew update
  brew tap homebrew/services
elif [[ "$os" == "$LINUX" ]]; then
  sudo apt update -y && 
  sudo apt upgrade -y &&
  sudo apt install -y \
  make \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  wget \
  curl \
  llvm \
  libncurses5-dev \
  libncursesw5-dev \
  xz-utils \
  tk-dev \
  libffi-dev \
  liblzma-dev \
  python-openssl \
  git \
  nodejs \
  npm
fi

# Enter the project
cd "$(dirname "$0")" && echo "Running in $(pwd)..." || exit 1

# Create directories for db backups, static files, and media files
mkdir -p .backups static media &>/dev/null

# If running with sudo, source .bashrc explicitly
if [ "$EUID" -e 0 ]; then
  source "$HOME/.bashrc"
fi

# Make sure pyenv is installed
echo "Checking for pyenv..."
pyenv --version &>/dev/null || {
  if [[ "$os" == "$MAC_OS" ]]; then
    brew install pyenv
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >>~/.bash_profile
  elif [[ "$os" == "$LINUX" ]]; then
    error "Install and configure pyenv (https://github.com/pyenv/pyenv), then rerun this script."
    exit 1
  fi
}
echo "Using $(pyenv --version)..."
echo "Installing required Python versions..."
while IFS= read -r pyversion; do
  if [[ -n $pyversion ]]; then
    pyenv install "$pyversion"
  fi
done < .python-version

# Node Version Manager (NVM)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
cd frontend && nvm install && nvm use && cd ..

# Make sure correct version of Python is used
echo "Checking Python version..."
python --version &>/dev/null || {
  error "Could not detect Python. Install Python 3.7 and rerun this script."
  exit 1
}
echo "Using $(python --version)..."

# Make sure Pip is installed
pip --version &>/dev/null || {
  error "Pip is not installed; unable to proceed."
  exit 1
}

# Install Poetry
poetry --version &>/dev/null || {
  echo "Installing Poetry..."
  # https://python-poetry.org/docs/#osx-linux-bashonwindows-install-instructions
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python &>/dev/null
  # shellcheck source=/dev/null
  source "$HOME/.poetry/env"
  poetry --version &>/dev/null || {
    echo "Unable to use Poetry's custom installer; falling back on pip..."
    # Update Pip
    pip install --upgrade pip &>/dev/null
    # Install Poetry with Pip
    pip install -U poetry
  }
  poetry_version=$(poetry --version)
  if [ -z "$poetry_version" ]; then
    echo "Error: Unable to install Poetry."
    exit 1
  fi
}
poetry self update &>/dev/null
echo "Using $(poetry --version)..."

# https://python-poetry.org/docs/configuration/
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true

if [[ ! "$skip_dependencies" == true ]]; then
  # Install dependencies with Poetry
  echo "Installing dependencies..."
  if [[ "$skip_dev_dependencies" == true ]]; then
    poetry install --no-dev --no-root || {
      error "Failed to install dependencies with Poetry."
      exit 1
    }
  else
    poetry install --no-root
  fi
fi

# Rclone: https://rclone.org/
rclone version &>/dev/null || {
  echo "Installing rclone ..."
  curl https://rclone.org/install.sh | sudo bash
}
mkdir -p $HOME/.config/rclone
cp config/rclone/rclone.conf $HOME/.config/rclone/rclone.conf

# Disable THP so it doesn't cause issues for Redis containers
echo "Disabling THP ..."
sudo bash -c "echo madvise > /sys/kernel/mm/transparent_hugepage/enabled"
# if test -f /sys/kernel/mm/transparent_hugepage/enabled; then
#    echo madvise > /sys/kernel/mm/transparent_hugepage/enabled
# fi

echo "Seeding database, environment vars, and media files (NOTE: This could take a long time!) ..."
poetry run invoke seed --remote

echo "Finished setup."
