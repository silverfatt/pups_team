class DateService {
  async getMonthName() {
    const response = await fetch('http://10.10.76.32:8000/api/v1/clients/grades_distribution', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    return data;
  }

  async getLineData() {
    const response = await fetch('http://10.10.76.32:8000/api/v1/clients/date_distribution', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    return data;
  }

  async getLineDataCurrent(number) {
    const response = await fetch(`http://10.10.76.32:8000/api/v1/clients/date_distribution_${number}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      return data;
  }

  async getReview(query) {
    const response = await fetch('http://10.10.76.32:8000/api/v1/clients/query_gigachat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
      }),
    });
    const data = await response.json();
    return data;
  }
}

const dateService = new DateService();

export default dateService;

