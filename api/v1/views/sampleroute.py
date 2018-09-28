#!/usr/bin/env python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from mongoengine.errors import OperationError, ValidationError, InvalidQueryError, LookUpError


@app_views.route('/sampleroute', methods=['GET', 'POST'])
def give_sample():
    '''
        sample route to avoid extra api calls
    '''
    return jsonify({"origin": "ChIJIQBpAG2ahYAR_6128GcTUEo",
                    "waypoints": ["ChIJx8sJFi9-j4ARZr3ycEr-4QU", 
                                  "ChIJHwlQOCJ-j4ARnUGwP7Y2lm0", 
                                  "ChIJiTRYUdV_j4ARa1aZMl9UX7g", 
                                  "ChIJD-xlgL-AhYARmMnFkJtQZFM", 
                                  "ChIJZfUix2N_j4ARs-PpAsrHQcc", 
                                  "ChIJn_eonYeAhYARB76FFdGjbYM", 
                                  "ChIJ6c9ZUdV_j4ARmMmO8UoIHPA", 
                                  "ChIJ-zVUQoiAhYAREEBQ1oqGsiE", 
                                  "ChIJ2UojPeqBhYAR6RgupRitcQM", 
                                  "ChIJffN_1hp-j4ART60fN2z-PBw", 
                                  "ChIJm5w05YOAhYARJQ97F36OeXo", 
                                  "ChIJdZAOFtN_j4AR2sktEphBjDg", 
                                  "ChIJkRcxr5uAhYARsnxbAw6evpI", 
                                  "ChIJdRXS7WKAhYARUcJF8EKJ4yE", 
                                  "ChIJn5nA9jx-j4ARBi3_fySrXNw", 
                                  "ChIJa53L8jZ_j4ARgqTmcxRA2o0", 
                                  "ChIJe-iBGISAhYARwuCnx_3hObA", 
                                  "ChIJw4KxxJqAhYARidJwCPR2Iw0", 
                                  "ChIJ6woYNYmAhYARZvMnYwdJYoA", 
                                  "ChIJDdLJ1o6AhYARsJXWNfy5J1k", 
                                  "ChIJPx7C6Dp-j4ARlZZ_LCU1hTs", 
                                  "ChIJxwBPDpuAhYAREmyxJOv11Nk", 
                                  "ChIJg8uN3iJ-j4AR3W84uTzK31E"]})
