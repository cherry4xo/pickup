'use client';
import { SliderFilledTrack, SliderThumb, SliderTrack, SimpleGrid, useToast, Divider, Select, Slider, VStack, HStack, Button, Input, Text, Box } from "@chakra-ui/react";
import { AnimatePresence, motion } from "framer-motion";
import { useSearchParams } from "next/navigation";
import { useState } from "react";

const fonts = [
  'Manrope Variable', 'Times New Roman', 'Montserrat'
];

const colors = [
  ['#000000', '#ffffff'],
  ['#000000', '#fff945'],
  ['#ff0000', '#ffffff'],
  ['#00b3ff', '#ffffff'],
  ['#ff0088', '#ffffff'],
  ['#7d12ae', '#ffffff'],
  ['#ffffff', '#000000'],
  ['#fff945', '#000000'],
  ['#ffffff', '#ff0000'],
  ['#ffffff', '#00b3ff'],
  ['#ffffff', '#ff0088'],
  ['#ffffff', '#7d12ae']
];

const toRadians = (degrees: number) => degrees * Math.PI / 180;

// enum Modes {
//   contour = 'Маркировка',
//   text = 'Брендирование'
// }

export default function Home() {
  const toast = useToast();
  const query = useSearchParams();

  const mode = query.get('mode') ?? 'contour';

  const [name, setName] = useState('');
  const [text, setText] = useState('');
  const [rawAngle, setRawAngle] = useState(90);
  const [border, setBorder] = useState(90);
  const [offsetX, setOffsetX] = useState(0);
  const [offsetY, setOffsetY] = useState(0);
  const [opacity, setOpacity] = useState(.5);
  const [fontSize, setFontSize] = useState(45);
  const [fontFamily, setFontFamily] = useState(fonts[0]);
  const [fontWeight, setFontWeight] = useState(300);
  const [colorScheme, setColorScheme] = useState(0);

  const size = 576;
  const r = (size - border) / 2;
  const angle = toRadians(rawAngle) - Math.PI * 2;

  const r_path = size / 2 - (border * .75);
  const center = size / 2;
  // const textLength = 2 * Math.PI * r_path; это тоже было для спейсинга букав

  function sendSample() {
    // @ts-ignore
    window.Telegram.WebApp.sendData(JSON.stringify({
      type: mode,
      title: name,
      font_text: fontFamily,
      font_size: fontSize,
      font_weight: fontWeight,
      border_color: colors[colorScheme][0],
      text_color: colors[colorScheme][1],
      angle: rawAngle,
      opacity,
      offsetX: 0,
      offsetY: 0,
      text,
      border
    }));

    toast({ status: 'success', title: 'Успешно', description: 'Шаблон сохранён!', duration: 3000, isClosable: true });
  }

  return <VStack w='100%' p='20px' align='center'>
    {/* <HStack w='100%' spacing='10px' justify='center'>
      {Object.keys(Modes).map((modeKey: string, i: number) => <Link key={i} w='50%' h='50px' href={`/?mode=${modeKey}`}>
        <Button w='100%' h='100%' bg={mode === modeKey ? 'blue.300' : 'gray.100'}>{Modes[modeKey as keyof typeof Modes]}</Button>
      </Link>)}
    </HStack> */}

    <AnimatePresence mode='wait'>
      <motion.div
        key={mode ?? 'none'}
        exit={{ opacity: 0 }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        style={{ width: '100%' }}
        transition={{ duration: .25, ease: 'easeInOut' }}
      >
        {mode
          ? <VStack w='100%' pb='40px' key={mode} minH='100vh' spacing='4vh'>
            <svg width={size} height={size} version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" style={{ transform: 'translateY(-60px) scale(.65)', marginBottom: '-130px' }}>
              <defs />

              {mode === 'contour'
                ? <ellipse rx={r} ry={r} cx={center} cy={center} fillOpacity="0" strokeWidth={border} strokeOpacity={opacity} stroke={colors[colorScheme][0]} />
                : <ellipse rx={r} ry={r} cx={center} cy={center} stroke='black' fillOpacity="0" strokeWidth={4} strokeOpacity={1} />}

              <path
                id="id1"
                fillOpacity={0}
                d={`M ${center * (1 - Math.cos(angle)) + border * .75 * Math.cos(angle)} ${center * (1 - Math.sin(angle)) + border * .75 * Math.sin(angle)}
                    A ${r_path} ${r_path} 0 1 1 ${center * (1 - Math.cos(angle + Math.PI)) + border * .75 * Math.cos(angle + Math.PI)} ${center * (1 - Math.sin(angle + Math.PI)) + border * .75 * Math.sin(angle + Math.PI)}
                    M ${center * (1 - Math.cos(angle + Math.PI)) + border * .75 * Math.cos(angle + Math.PI)} ${center * (1 - Math.sin(angle + Math.PI)) + border * .75 * Math.sin(angle + Math.PI)}
                    A ${r_path} ${r_path} 0 1 1 ${center * (1 - Math.cos(angle)) + border * .75 * Math.cos(angle)} ${center * (1 - Math.sin(angle)) + border * .75 * Math.sin(angle)}`}
              />

              {mode === 'contour'
              // вот это было здесь lengthAdjust="spacing" textLength={textLength} 
                ? <text fill={colors[colorScheme][1]} style={{ fontSize, fontFamily, fontWeight }}>
                  <textPath xlinkHref="#id1">{text + '‎'}</textPath>
                </text>
                : <image width={size} height={size} href='/logo.jpg' x={offsetX + size * .1} y={offsetY + size * .1} style={{ opacity, position: 'absolute', transform: 'scale(.833)' }} />}
            </svg>

            <VStack w='100%'>
              <Text w='100%'>Введите название шаблона</Text>
              <Input w='100%' value={name} placeholder='Шаблон 1' onChange={(e: any) => setName(e.target.value)} />
            </VStack>

            {mode === 'contour'
              ? <>
                <VStack w='100%'>
                  <Text w='100%'>Текст на кружочке</Text>
                  <Input w='100%' value={text} placeholder='Какой-то текст' onChange={(e: any) => setText(e.target.value)} />
                </VStack>

                <VStack w='100%'>
                  <Text w='100%'>Шрифт текста</Text>
                  <Select w='100%' value={fontFamily} onChange={(e: any) => setFontFamily(e.target.value)}>
                    {fonts.map((font: string, i: number) => <option key={i} value={font}>{font}</option>)}
                  </Select>
                </VStack>

                {[
                  { label: 'Размер шрифта', props: { min: 10, step: 1, max: 100, value: fontSize, onChange: (e: number) => setFontSize(e) } },
                  { label: 'Жирность шрифта', props: { min: 300, step: 100, max: 800, value: fontWeight, onChange: (e: number) => setFontWeight(e) } },
                  { label: 'Толщина обводки', props: { min: 10, step: 1, max: 200, value: border, onChange: (e: number) => setBorder(e) } },
                  { label: 'Прозрачность обводки', props: { min: 0, step: .01, max: 1, value: opacity, onChange: (e: number) => setOpacity(e) } },
                  { label: 'Угол', props: { min: 0, step: 1, max: 360, value: rawAngle, onChange: (e: number) => setRawAngle(e) } },
                ].map((slider: any, i: number) => <VStack key={i} w='100%'>
                  <Text>{slider.label}</Text>
                  <Slider w='100%' aria-label='slider-ex-1' {...slider.props}>
                    <SliderTrack>
                      <SliderFilledTrack />
                    </SliderTrack>
                    <SliderThumb />
                  </Slider>
                </VStack>)}

                <VStack w='100%'>
                  <Text>Цвета</Text>
                  <SimpleGrid columns={3} spacing='8px'>
                    {colors.map((chunk: string[], i: number) => <HStack key={i} p='6px' spacing={0} borderRadius='200px' border='1px solid gray' onClick={() => setColorScheme(i)} bg={colorScheme === i ? 'gray.400' : 'white'} _hover={{ bg: colorScheme === i ? 'gray.400' : 'gray.200', cursor: 'pointer' }}>
                      <Box w='20px' h='20px' bg={chunk[0]} borderRadius='200px 0 0 200px' />
                      <Box w='20px' h='20px' bg={chunk[1]} borderRadius='0 200px 200px 0' />
                    </HStack>)}
                  </SimpleGrid>
                </VStack>
              </>
              : <>
                {/* <VStack w='100%'>
                  <Text w='100%'>Картинка для наложения</Text>
                  <Input type='file' onChange={(e: any) => setImg(URL.createObjectURL(e.target.files[0]))} />
                </VStack> */}

                {[
                  { label: 'Прозрачность', props: { min: 0, step: .01, max: 1, value: opacity, onChange: (e: number) => setOpacity(e) } }
                ].map((slider: any, i: number) => <VStack key={i} w='100%'>
                  <Text>{slider.label}</Text>
                  <Slider w='100%' aria-label='slider-ex-1' {...slider.props}>
                    <SliderTrack>
                      <SliderFilledTrack />
                    </SliderTrack>
                    <SliderThumb />
                  </Slider>
                </VStack>)}
              </>}

            <Button w='100%' colorScheme='blue' onClick={sendSample}>Сохранить</Button>
          </VStack>
          : <Text w='100%' key='none' minH='100vh'>Выберите тип шаблона</Text>}
      </motion.div>
    </AnimatePresence>
  </VStack>
}
