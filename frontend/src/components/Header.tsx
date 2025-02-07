import React from 'react';
import { AppBar, Container, Toolbar, Typography } from '@mui/material';

interface HeaderProps {
  name: string;
  title: string;
}

const Header: React.FC<HeaderProps> = ({ name, title }) => {
  return (
    <AppBar position="static" color="primary" elevation={0}>
      <Toolbar>
        <Container maxWidth="lg">
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
            {name}
          </Typography>
          <Typography variant="h6" color="inherit" sx={{ mt: 1 }}>
            {title}
          </Typography>
        </Container>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
