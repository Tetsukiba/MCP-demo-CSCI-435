import { render } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('renders without crashing', () => {
    render(<LoginForm />);
  });
});
