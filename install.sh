url='https://github.com/DuTra01/CheckUser'

cd ~

if ! [ -x "$(command -v git)" ]; then
    echo 'Erro: git nao esta instalado.' >&2
    echo 'Instalando Git...'

    sudo apt-get install git -y 1>/dev/null 2>/dev/null

    echo 'Git instalado com sucesso.'
fi

function install_checkuser() {
    echo 'Instalando CheckUser...'

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
        echo 'CheckUser nao esta instalado.'
        exit 1
    fi

    echo 'Verificando atualizacoes...'
    cd CheckUser

    git fetch --all
    git reset --hard origin/master
    git pull origin master

    python3 setup.py install
    echo 'CheckUser atualizado com sucesso.'
}

function uninstall_checkuser() {
    echo 'Desinstalando CheckUser...'

    [[ -d CheckUser ]] && rm -rf CheckUser

    [[ -f /usr/bin/checker ]] && {
        service checker stop
        /usr/bin/checker --uninstall
        rm /usr/bin/checker
    }

    [[ -f /usr/local/bin/checker ]] && {
        service checker stop
        /usr/local/bin/checker --remove-service
        rm /usr/local/bin/checker
    }
}

function console_menu() {
    clear
    echo 'CHECKUSER MENU'
    echo '[01] - Instalar CheckUser'
    echo '[02] - Atualizar CheckUser'
    echo '[03] - Desinstalar CheckUser'
    echo '[00] - Sair'

    read -p 'Escolha uma opção: ' option

    case $option in
    01 | 1)
        install_checkuser
        console_menu
        ;;
    02 | 2)
        check_update
        console_menu
        ;;
    03 | 3)
        uninstall_checkuser
        console_menu
        ;;
    00 | 0)
        echo 'Saindo...'
        exit 0
        ;;
    *)
        echo 'Opção inválida.'
        read -p 'Pressione enter para continuar...'
        console_menu
        ;;
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
