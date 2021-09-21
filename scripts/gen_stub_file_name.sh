#!/bin/zsh

set -eu

CMDNAME=`basename $0`

FLG_COMMENT="FALSE"
FLG_POST="FALSE"
while getopts c:p: OPT
do
  case $OPT in
    c ) FLG_COMMENT="TRUE"; COMMENT_ID="$OPTARG" ;;
    p ) FLG_POST="TRUE" ; POST_ID="$OPTARG" ;;
  esac
done

SCRIPT_DIR=`dirname $0`
PROJECT_DIR=$SCRIPT_DIR/..
STUB_DIR=$PROJECT_DIR/tests/stubs

shift $((OPTIND - 1))

TARGET_PATH=`echo $1 | sed -e "s/\/v1\///g"`
REPLACED=`echo $TARGET_PATH | sed -e "s/:team_name/docs/g"`

if [ "$FLG_POST" = "TRUE" ]; then
    REPLACED=`echo $REPLACED | sed -e "s/:post_number/$POST_ID/g"`
fi

if [ "$FLG_COMMENT" = "TRUE" ]; then
    REPLACED=`echo $REPLACED | sed -e "s/:comment_id/$COMMENT_ID/g"`
fi

REPLACED=`echo $REPLACED | sed -e "s/\//_/g"`
echo "$STUB_DIR/$REPLACED.json"
code "$STUB_DIR/$REPLACED.json"
