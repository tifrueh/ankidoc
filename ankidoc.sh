#!/bin/sh

help="Usage: ${0} [ qls ] <file> ..."

qlist=0

argv0="${0}"

header='#separator semicolon
#html true
#columns id;question;answer

'

function generate_card() {
    card_path="${1}"
    file_name="${card_path##*/}"
    card_id="${file_name%.*}"
    card_front="${card_path%.*}.front"
    card_back="${card_path%.*}.back"

    if ! [ -f $card_front ]; then
        printf '%s' "${argv0}: ${card_front} not found" 1>&2
        exit 1
    elif ! [ -f $card_back ]; then
        printf '%s' "${argv0}: ${card_back} not found" 1>&2
        exit 1
    fi

    front_html="$(asciidoctor -e -o - ${card_front} | sed -e 's/"/""/g')"
    back_html="$(asciidoctor -e -o - ${card_back} | sed -e 's/"/""/g')"

    printf '"%s";"%s";"%s"' "${card_id}" "${front_html}" "${back_html}"
}

function generate_all() {

    printf '%s' "${header}"

    for file in $@; do
        if [ ${file##*.} = "front" ] || [ ${file##*.} = "back" ]; then
            printf '%s\n' "$(generate_card ${file})"
        else
            printf '%s\n' "${argv0}: not processing ${file}" 1>&2
            continue
        fi
    done
}

function qlist() {
    for file in $@; do
        if [ ${file##*.} = "front" ]; then
            printf '%s : %s\n' "${file}" "$(cat ${file})"
        fi
    done
}

if [ "${1}" = "qls" ]; then
    qlist=1
    shift
fi

for file in $@; do
    if ! [ -f $file ]; then
        printf '%s\n' "${help}"
        exit 1
    fi
done

if [ $qlist -eq 1 ]; then
    qlist $@
else
    generate_all $@
fi
