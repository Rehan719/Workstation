import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';
import QEPScreen from './src/screens/QEPScreen';
import { Book, Layout, Settings } from 'lucide-react-native';
import { View, Text } from 'react-native';

const Tab = createBottomTabNavigator();

const Placeholder = ({ name }) => (
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    <Text>Jules AI {name} v118.0</Text>
  </View>
);

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          tabBarActiveTintColor: '#C9A86B',
          tabBarInactiveTintColor: '#1E2A47',
          headerStyle: { backgroundColor: '#1E2A47' },
          headerTintColor: '#FFF',
          headerTitleStyle: { fontWeight: 'bold' },
        }}
      >
        <Tab.Screen
          name="Dashboard"
          component={() => <Placeholder name="Dashboard" />}
          options={{ tabBarIcon: ({ color }) => <Layout color={color} size={24} /> }}
        />
        <Tab.Screen
          name="QEP"
          component={QEPScreen}
          options={{
            title: 'Quranic Education',
            tabBarIcon: ({ color }) => <Book color={color} size={24} />
          }}
        />
        <Tab.Screen
          name="Settings"
          component={() => <Placeholder name="Settings" />}
          options={{ tabBarIcon: ({ color }) => <Settings color={color} size={24} /> }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
