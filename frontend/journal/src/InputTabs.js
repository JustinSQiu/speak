import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import AudioRecorder from './AudioRecorder';
import VideoRecorder from './VideoRecorder';
import TextMemo from './TextMemo';
import SearchBar from './SearchBar';
import Upload from './Upload';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

export default function BasicTabs() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: '100%' }}>
        <Tabs value={value} onChange={handleChange} aria-label="basic tabs example" centered>
          <Tab label="Upload a New Recording" {...a11yProps(0)} />
          <Tab label="Write a New Entry" {...a11yProps(1)}/>
          <Tab label="Search" {...a11yProps(2)} />
        </Tabs>
      <TabPanel value={value} index={0}>
        <Upload />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <TextMemo />
      </TabPanel>
      <TabPanel value={value} index={2}>
        <SearchBar />
      </TabPanel>
    </Box>
  );
}
