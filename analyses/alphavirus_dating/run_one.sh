HOST_SCENARIO=$1
VIRUS_SCENARIO=$2
USE_CLOCK=$3
BOUND_AGE=$4
UPDATE_ROOT=$5
NO_CALIB=$6
UNDER_PRIOR=$7
DROP_WEEV=$8
ONE_PER=$9

RB_INIT="host_scenario=\"${HOST_SCENARIO}\"; virus_scenario=\"${VIRUS_SCENARIO}\"; use_empirical_clock=${USE_CLOCK}; bound_max_age=${BOUND_AGE}; update_root=${UPDATE_ROOT};no_calib=${NO_CALIB}; under_prior=${UNDER_PRIOR}; drop_weev=${DROP_WEEV}; one_per=${ONE_PER}; source(\"run_inf.Rev\")"
echo $RB_INIT

echo $RB_INIT | rb
