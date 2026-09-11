# Flask_Hospital_Bookings-

A Flask + SQLAlchemy hospital appointment-booking app: patients register, log in, and book a slot
with a doctor in a given department.

All source lives under the `hospital system/` directory (note the space in the name).

## What it does

Routes in `hospital system/app/routes.py`:

| Route | Purpose |
| --- | --- |
| `/` | Landing page |
| `/signup`, `/login`, `/logout` | Accounts. Signup takes a `usertype` (Doctor / Patient); bcrypt hashes the password |
| `/doctors` | Form to add a doctor (email, name, department) |
| `/patients` | Booking form — email, name, gender, slot, disease, time, date, department, 10-digit phone. Department choices are populated from the `doctors` table |
| `/bookings` | Intended to list a user's bookings |
| `/edit/<pid>`, `/delete/<pid>` | Edit/delete a patient booking |
| `/details` | Dumps the `trigr` audit table |
| `/search` | Checks whether a doctor name exists and flashes "Available" / "Not Available" |
| `/test` | Health check — returns "My database is Connected" or not |

### Data model (`app/models.py`)

`User` (id, username, usertype, email, password), `Patients` (booking records), `Doctors`,
`Trigr` (an audit-trail table: pid, email, name, action, timestamp), and an unused `Test` table.

**The `trigr` table is never written to by any Python code.** It is named after a database *trigger*,
which suggests the original design logged actions at the SQL level. No trigger is defined in the
committed Alembic migration, so `/details` will always render an empty list.

## Tech stack

Python 3.12, Flask, Flask-SQLAlchemy, Flask-Migrate/Alembic, Flask-Login, Flask-Bcrypt,
Flask-WTF + WTForms, Jinja2, Bootstrap. Database: SQLite by default
(`sqlite:///hosi_mgmt_ssm.db`), overridable via the `DATABASE_URL` environment variable.

## Setup

**There is no `requirements.txt` in this repo.** From the imports you need at least:

```bash
python3 -m venv venv && source venv/bin/activate
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-Login Flask-Bcrypt Flask-WTF WTForms email-validator
```

`app/__init__.py` also does `import stripe` and `import paypalrestsdk` at module level even though no
payment code exists anywhere in the app, so you must install those two as well or delete the imports:

```bash
pip install stripe paypalrestsdk
```

### Run

```bash
cd "hospital system"
python run.py
```

**The app listens on port 10000**, not the Flask default — open <http://127.0.0.1:10000>.

Set `SECRET_KEY` in the environment; `config.py` otherwise falls back to a hardcoded default
(literally `do_not_show_this_to_anyone_100`).

## Known bugs

These are in the committed code and will raise at runtime:

- **`/doctors`** builds a `DoctorForm(...)` and passes it to `db.session.add()` instead of
  constructing a `Doctors` model. Adding a doctor cannot work — which is consistent with the
  committed database having zero rows in `doctors`. Because `/patients` populates its department
  dropdown from `Doctors.query.all()`, **no bookings can be made until this is fixed**.
- **`/bookings`** queries `Doctors.query.filter_by(user_id=current_user.did)`. `Doctors` has no
  `user_id` column and `User` has no `did` attribute.
- **`/edit/<string:pid>`** and **`/delete/<string:pid>`** declare a URL parameter named `pid` but the
  view functions are `def edit(email)` and `def delete(email)`. Flask will raise a `TypeError` on
  dispatch, and `delete()` additionally references an undefined `pid`.
- `/search` assigns `dept = Doctors.query.filter_by(dept=query).first()` and never uses it.

## Repository contents worth knowing about

- **`hospital system/instance/hosi_mgmt_ssm.db` is a committed SQLite database** containing two real
  user accounts with email addresses and bcrypt password hashes. See the security note below.
- **`hospital system/app/debug.py`** (434 lines) is a scratch file: a pasted Python traceback
  followed by copy-pasted duplicates of `models.py`, `forms.py` and `routes.py`. It is not imported
  by anything and should be deleted. The traceback contains local filesystem paths from the author's
  machine.
- That traceback references a source directory named `Hospital-Management-System-dbmsminiproject-main`,
  which suggests this project was **derived from an existing open-source hospital-management
  project** rather than written from scratch. **TODO: verify the upstream source and add attribution
  plus its licence terms**, since the current `LICENSE` (GPL-3.0) may not be compatible with it.
- `__pycache__/*.pyc` files are committed. There is no `.gitignore`.

## Security / privacy

⚠️ The committed SQLite database exposes two accounts, including a **personal email address**
(`joelharold@ymail.com`) and a second user's address, together with their bcrypt hashes. Delete the
`.db` from the repository and from git history, add `instance/` and `*.db` to a `.gitignore`, and
change those passwords wherever they are reused.

## Status

**Broken prototype.** Last commit August 2024. Signup, login and the patient-booking form are
implemented, but the doctor-creation bug blocks the main flow and several routes raise on dispatch.

## Licence

GPL-3.0 (see `LICENSE`) — but see the attribution note above.
