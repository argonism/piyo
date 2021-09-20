set -eu

SCRIPT_DIR=`dirname $0`
PROJECT_DIR=$SCRIPT_DIR/..

cd $PROJECT_DIR
# TEST_FILES=tests/test_*
# for file_path in $TEST_FILES; do
#     FILENAME=`basename $file_path`
#     echo "\n\ntest: $FILENAME\n"
#     python3 -m unittest $file_path -v
# done

# python3 -m unittest tests/test_* -v
python3 tests/test_team_endpoint.py -v