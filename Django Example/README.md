# WorqHat AI Django Example

This is a simple Django application that demonstrates how to integrate with the WorqHat AI API.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
- Copy the `.env.example` file to `.env`
- Replace `your_api_key_here` with your actual WorqHat API key

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Visit http://localhost:8000 in your browser

## Usage

1. Enter your prompt in the text area
2. Click "Generate Response"
3. The AI-generated response will appear below

## Features

- Simple web interface
- Integration with WorqHat AI API
- Async response handling
- Error handling and display
- Loading state indication

## Security Note

Make sure to never commit your actual API key to version control. The `.env` file is included in `.gitignore` for this reason.
