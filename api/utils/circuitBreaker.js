class CircuitBreaker {
  constructor({ failureThreshold = 3, successThreshold = 2, timeout = 10000 }) {
    this.failureThreshold = failureThreshold;
    this.successThreshold = successThreshold;
    this.timeout = timeout;
    this.state = 'CLOSED';
    this.failureCount = 0;
    this.successCount = 0;
    this.nextAttempt = Date.now();
  }

  async callService(requestFn) {
    if (this.state === 'OPEN') {
      if (Date.now() > this.nextAttempt) {
        this.state = 'HALF-OPEN';
      } else {
        throw new Error('Service unavailable - Circuit Breaker open');
      }
    }

    try {
      const response = await requestFn();
      if (this.state === 'HALF-OPEN') {
        this.successCount++;
        if (this.successCount >= this.successThreshold) {
          this.reset();
        }
      }
      return response;
    } catch (error) {
      this.failureCount++;
      if (
        this.failureCount >= this.failureThreshold ||
        this.state === 'HALF-OPEN'
      ) {
        this.trip();
      }
      throw error;
    }
  }

  trip() {
    this.state = 'OPEN';
    this.nextAttempt = Date.now() + this.timeout;
    this.failureCount = 0;
    this.successCount = 0;
  }

  reset() {
    this.state = 'CLOSED';
    this.failureCount = 0;
    this.successCount = 0;
  }
}

module.exports = CircuitBreaker;