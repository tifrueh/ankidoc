#!/bin/zsh

help="Usage: ${0} <directory>"

if [ $# -ne 1 ]; then
    echo $help 1>&2
    exit 1
elif ! [ -d "${1}" ]; then
    echo $help 1>&2
    exit 1
fi

dir="${1}"
argv0="${0}"

cd "${dir}"

header="#separator semicolon\n#html true\n#columns id;question;answer\n"

function generate_card() {
    cards_dir=$1
    card_id=$2
    card_front="${cards_dir}/${card_id}.front"
    card_back="${cards_dir}/${card_id}.back"

    if ! [ -f $card_front ]; then
        echo "${argv0}: ${card_front} not found" 1>&2
        exit 1
    elif ! [ -f $card_back ]; then
        echo "${argv0}: ${card_back} not found" 1>&2
        exit 1
    fi

    front_html="$(asciidoctor -e -o - ${card_front} | sed -e 's/"/""/g')"
    back_html="$(asciidoctor -e -o - ${card_back} | sed -e 's/"/""/g')"

    printf '"%s";"%s";"%s"' "${card_id}" "${front_html}" "${back_html}"
}

echo $header

for file in *; do
    if [ ${file##*.} = "front" ]; then
        printf '%s\n' "$(generate_card . ${file%.front})"
    elif [ ${file##*.} = "back" ]; then
        continue
    else
        echo "${argv0}: not processing ${file}" 1>&2
        continue
    fi
done
