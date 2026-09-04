const { test, expect } = require('@playwright/test');

test('Placement Readiness Digital Twin - full interaction test', async ({ page }) => {
  // 1. Navigate to Streamlit app
  await page.goto('http://localhost:8501', { waitUntil: 'networkidle' });
  
  // 2. Check title and headers
  await expect(page).toHaveTitle(/Placement Readiness Digital Twin|Streamlit/i);
  await expect(page.getByText('Placement Readiness Digital Twin')).toBeVisible();
  await expect(page.getByText('Predict placement readiness and company fit.')).toBeVisible();
  
  // 3. Take screenshot of initial state
  await page.screenshot({ path: 'tests/initial_state.png', fullPage: true });

  // 4. Click the 'Predict Placement Readiness' button
  const predictBtn = page.getByRole('button', { name: /Predict Placement Readiness/i });
  await expect(predictBtn).toBeVisible();
  await predictBtn.click();

  // 5. Verify results
  await expect(page.getByText('Prediction Result')).toBeVisible({ timeout: 15000 });
  await expect(page.getByText('Readiness Score')).toBeVisible();
  await expect(page.getByText('Prediction Confidence')).toBeVisible();
  await expect(page.getByText('Top Company Matches')).toBeVisible();

  // 6. Verify specific companies appear
  await expect(page.getByText(/Microsoft:/)).toBeVisible();
  await expect(page.getByText(/Google:/)).toBeVisible();
  await expect(page.getByText(/Amazon:/)).toBeVisible();

  // 7. Take full page screenshot of the prediction results
  await page.screenshot({ path: 'tests/prediction_result.png', fullPage: true });
  console.log('TEST_PASSED_SUCCESSFULLY');
});
