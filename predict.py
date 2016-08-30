"""
Uncomment methods to predict with.

Commments after or above functions describe their effects.
"""

from main import (
    chief_complaint,
    distress_level,
    formulation,
    history_and_precipitating_events,
)

from word_stem_svm import word_stem_predict
from numeric_svm import numeric_svm_predict


# word_stem_predict(history_and_precipitating_events) # Always predicts MILD.
# word_stem_predict(chief_complaint) # Always predicts MILD.
# word_stem_predict(formulation) # Always predicts MILD.

# Gets between 30% - 40% accuracy overguesses MILD, rarely guesses Absent
# numeric_svm_predict(distress_level)

# Gets between 40% - 45% accuracy overguesses MILD, rarely guesses Absent
#numeric_svm_predict(distress_level, ignore_values=[26.0])

# Gets between 40% - 45% accuracy overguesses MODERATE, rarely guesses Absent
#numeric_svm_predict(distress_level, ignore_class=["MILD"])


#############################################################################
# TODO: Need to check the "actual" values in the the accuracy tracker and in
# turn need to check the accuracy. Need to account for ignore_value in tracker
#############################################################################
#numeric_svm_predict(distress_level, ignore_values=[26.0], ignore_class=["MILD"])

# Between 30 to 100 percent accuracy close to 70% - 80%.
#numeric_svm_predict(distress_level, 50, ignore_values=[26.0], ignore_class=["MILD", "MODERATE"])

numeric_svm_predict(distress_level, 50, ignore_class=["MILD", "MODERATE"])
