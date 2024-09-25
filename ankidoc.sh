#!/bin/sh

qlist=0
asciigen=0

progname="${0##*/}"

help="Usage: ${progname} [ qls | asciigen ] <file> ..."

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
        printf '%s\n' "${progname}: ${card_front} not found" 1>&2
        exit 1
    elif ! [ -f $card_back ]; then
        printf '%s\n' "${progname}: ${card_back} not found" 1>&2
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
            printf '%s\n' "${progname}: not processing ${file}" 1>&2
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

function asciigen() {
    card_path="${1}"
    card_front="${card_path%.*}.front"
    card_back="${card_path%.*}.back"

    if ! [ -f $card_front ]; then
        printf '%s\n' "${progname}: ${card_front} not found" 1>&2
        exit 1
    elif ! [ -f $card_back ]; then
        printf '%s\n' "${progname}: ${card_back} not found" 1>&2
        exit 1
    fi

    printf '\n%s\n\n%s\n' "$(cat ${card_front})" "$(cat ${card_back})"
}

function asciigen_all() {
    for file in $@; do
        if [ ${file##*.} = "front" ] || [ ${file##*.} = "back" ]; then
            printf '%s\n' "$(asciigen ${file})"
        else
            printf '%s\n' "${progname}: not processing ${file}" 1>&2
            continue
        fi
    done
}

if [ "${1}" = "qls" ]; then
    qlist=1
    shift
fi

if [ "${1}" = "asciigen" ]; then
    asciigen=1
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
elif [ $asciigen -eq 1 ]; then
    asciigen_all $@
else
    generate_all $@
fi
