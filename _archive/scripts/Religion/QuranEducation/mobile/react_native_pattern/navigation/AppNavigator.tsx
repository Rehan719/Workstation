import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { View, Text } from 'react-native';

const Tab = createBottomTabNavigator();

const CurriculumScreen = () => <View><Text>Curriculum</Text></View>;
const HifzScreen = () => <View><Text>Hifz Tracker</Text></View>;
const ProfileScreen = () => <View><Text>Student Profile</Text></View>;

const AppNavigator = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Curriculum" component={CurriculumScreen} />
      <Tab.Screen name="Hifz" component={HifzScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

export default AppNavigator;
