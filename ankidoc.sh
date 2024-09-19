#!/bin/sh

help="Usage: ${0} <directory>"

if [ $# -eq 2 ]; then
    echo $help
    exit 1
elif ! [ -d $1 ]; then
    echo $help
    exit 1
fi

dir=$1
argv0=$0

cd $dir

header="#separator semicolon\n#html true\n#columns id;question;answer\n"

function generate_card() {
    cards_dir=$1
    card_id=$2
    card_front="${cards_dir}/${card_id}.front"
    card_back="${cards_dir}/${card_id}.back"

    if ! [ -f $card_front ]; then
        echo "${argv0}: ${card_front} not found"
        exit 1
    elif ! [ -f $card_back ]; then
        echo "${argv0}: ${card_back} not found"
        exit 1
    fi

    front_html=$(asciidoctor -e -o - ${card_front} | sed 's/"/""/g' | tr -d '\n')
    back_html=$(asciidoctor -e -o - ${card_back} | sed 's/"/""/g' | tr -d '\n')

    echo "\"${card_id}\";\"${front_html}\";\"${back_html}\""
}

echo $header

for file in *; do
    if [ ${file##*.} = "front" ]; then
        echo $(generate_card . ${file%.front})
    elif [ ${file##*.} = "back" ]; then
        continue
    else
        echo "${argv0}: not processing ${file}"
        continue
    fi
done
