import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, SPACING, FONT_SIZES } from '../utils/constants';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.BACKGROUND,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    fontSize: FONT_SIZES.LG,
    color: COLORS.TEXT_SECONDARY,
  },
});

export default function Screen() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>${screen}</Text>
      <Text style={[styles.text, { marginTop: SPACING.MD }]}>
        Coming soon...
      </Text>
    </View>
  );
}
