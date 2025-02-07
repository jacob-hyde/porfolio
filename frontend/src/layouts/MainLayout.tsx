import React from 'react';
import { Box, CssBaseline, ThemeProvider } from '@mui/material';
import { Outlet } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useAppSelector } from '../hooks';
import { theme } from '../theme';

interface MainLayoutProps {
}

const MainLayout: React.FC<MainLayoutProps> = () => {
  const { profile } = useAppSelector((state) => state.portfolio);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          minHeight: '100vh',
          bgcolor: 'background.default',
        }}
      >
        {profile && <Header name={profile.name} title={profile.title} />}
        <Box component="main" sx={{ flexGrow: 1 }}>
          <Outlet />
        </Box>
        <Footer />
      </Box>
    </ThemeProvider>
  );
};

export default MainLayout;
