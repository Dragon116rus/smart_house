# TP-Link Monitor

This project monitors the availability of a TP-Link router and pushes the data to VictoriaMetrics for monitoring and visualization.

## Project Structure

```
tp-link-monitor
├── src
│   ├── main.py                # Entry point of the application
│   ├── router
│   │   ├── __init__.py        # Marks the router directory as a package
│   │   └── tp_link_client.py   # Handles communication with the TP-Link router
│   ├── metrics
│   │   ├── __init__.py        # Marks the metrics directory as a package
│   │   └── victoria_metrics_client.py # Handles connection to VictoriaMetrics
│   └── utils
│       ├── __init__.py        # Marks the utils directory as a package
│       └── helpers.py         # Contains utility functions
├── requirements.txt            # Lists project dependencies
├── .env.example                # Example of environment variables
└── README.md                   # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd tp-link-monitor
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env` and fill in the required values for your TP-Link router and VictoriaMetrics endpoint.

## Usage

To run the application, execute the following command:
```
python src/main.py
```

This will initialize the router client, check the availability of the TP-Link router, and push the data to VictoriaMetrics.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.