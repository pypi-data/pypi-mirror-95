#!/bin/bash

unit_tests=(\
 test_001_create_db\
 test_002_fura_library\
)

function run_suit()
{
  local ut_idx=1
  local ut_name=
  local ut_cnt=${#unit_tests[@]}

  for ut in ${unit_tests[*]}; do

    ut_name="${ut}.py"

    if [ ! -f "$ut_name" ]; then
      mlib_raise "$0" "$LINENO" "Unit-Test not found. [idx:${ut_idx}, name:${ut_name}]"
    fi

    mlib_eclo "Unit-Test [${ut_idx}/${ut_cnt} : ${ut}] - start"

    mlib_exec "$0" "$LINENO" "python ${ut_name}"

    mlib_eclo "Unit-Test [${ut_idx}/${ut_cnt} : ${ut}] - done"

    ((ut_idx++))
  done

}

function init_externals()
{
  if [ ! -f "${LOCAL_PATH}/externs/mettle/bash/mettle-lib.sh" ]; then
    echo ""
    echo "ERROR! Mettle bash library not found! [\${LOCAL_PATH}/externs/mettle/bash/mettle-lib.sh]"
    echo ""
    exit 1
  fi

  source "${LOCAL_PATH}/externs/mettle/bash/mettle-lib.sh"
  source "${LOCAL_PATH}/externs/mettle/bash/mettle-platform.sh"
}


function usage_and_exit()
{
  echo ""
  echo " BS-FURA Unit-Test Suite"
  echo ""
  echo "Usage: $0 [ -? ]"
  echo "---------------------------------------------------------------------"
  echo " -?    : This help"
  echo ""
  echo ""

  exit 2
}


function main()
{
  init_externals

  rm -f ./dax-ut.log

  mlib_logger_init "bs_fura-ut" "debug" "."

  run_suit
}


while getopts "ir" opt; do
  case $opt in
    \?)
      usage_and_exit
      ;;
    *)
      usage_and_exit
      ;;
  esac
done

main
