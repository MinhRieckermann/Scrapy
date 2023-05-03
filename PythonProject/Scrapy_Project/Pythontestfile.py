import pandas as pd

import pandas as pd

data = {'id': ['id0219696', 'id1372182', 'id3569980', 'id2858528'],
        'vendor_id': [72, 80, 69, 29],
        'pickup_datetime': ['2016-06-06 06:06:20', '2016-02-07 19:18:49', '2016-06-14 00:26:11', None],
        'dropoff_datetime': ['2016-06-06 06:13:34', None, '2016-06-14 00:34:09', None]}

df = pd.DataFrame(data)

print(df)