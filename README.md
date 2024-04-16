# Throttle model experimentation

In this little script I experiment with the calculation of torque and power curves for partially open throttle (at 10%, 20% etc). Currently it's only using a simple weighted average between full throttle torque and a hardcoded no throttle torque, but the purpose is to experiment with other models.

## Inspiration

- [BeamNG article about their throttle model](https://www.beamng.com/game/news/blog/throttle-torque-curves/)
- Example torque curve used is a 5th gen Honda Civic, yoinked from [automobile-catalog](https://www.automobile-catalog.com/browse.php)


## Usage

Only dependency is Python 3, pip and virtualenv.

```sh
# From project root directory
python -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
python main.py --help
```

You can define a torque curve at the top of `main.py` as a list of (rpm, torque in Nm) tuples. This curve is at full throttle. The script takes care of the rest.
