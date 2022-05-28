url='https://github.com/DuTra01/CheckUser'

cd ~

if ! [ -x "$(command -v git)" ]; then
    echo 'Error: git is not installed.' >&2
    exit 1
fi

function install_checkuser() {
    echo 'Installing CheckUser...'

    git clone $url
    cd CheckUser

    python3 setup.py install

    clear
    read -p 'Porta: ' -e -i 5000 port
    checker --config-port $port --create-service
    service check_user start

    echo 'URL: http://'$(curl -s icanhazip.com)':'$port
}

function check_update() {
    if ! [ -d CheckUser ]; then
        echo 'CheckUser is not installed.'
        exit 1
    fi

    echo 'Checking for updates...'
    cd CheckUser

    git fetch --all
    git reset --hard origin/master
    git pull origin master

    python3 setup.py install
    echo 'Update complete.'
}

function uninstall_checkuser() {
    echo 'Uninstalling CheckUser...'

    [[ -d CheckUser ]] && rm -rf CheckUser
    [[ -f /usr/local/bin/checker ]] && {
        service checker stop
        /usr/local/bin/checker --remove-service
        rm /usr/local/bin/checker
    }
}

function console_menu() {
    clear
    echo 'CheckUser Console Menu'
    echo '[01] - Instalar CheckUser'
    echo '[02] - Atualizar CheckUser'
    echo '[03] - Desinstalar CheckUser'
    echo '[00] - Sair'

    read -p 'Escolha uma opção: ' option

    case $option in
    01 | 1) install_checkuser ;;
    02 | 2) check_update ;;
    03 | 3) uninstall_checkuser ;;
    00 | 0) exit 0 ;;
    *) echo 'Opção inválida.' ;;
    esac

}

function main() {
    case $1 in
    install)
        install_checkuser
        ;;
    update)
        check_update
        ;;
    uninstall)
        uninstall_checkuser
        ;;
    *)
        echo 'Usage: ./install.sh [install|update|uninstall]'
        exit 1
        ;;
    esac
}

if [[ $# -eq 0 ]]; then
    console_menu
else
    main $1
fi
